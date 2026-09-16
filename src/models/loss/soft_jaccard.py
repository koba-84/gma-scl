from __future__ import annotations

import torch
import torch.nn.functional as functional
from torch import nn

from src.models.loss.components.label_overlap import compute_or_counts


def _compute_soft_jaccard_loss(
    z: torch.Tensor,
    labels: torch.Tensor,
    *,
    student_temperature: float,
    teacher_temperature: float,
) -> torch.Tensor:
    """Soft-Jaccard contrastive loss.

    Difference from Base:
    - Base uses Jaccard as positive weights and ignores zero-overlap pairs.
    - Soft-Jaccard uses Jaccard to construct a dense teacher distribution q_ij.

    q_ij = softmax(Jaccard(Y_i, Y_j) / teacher_temperature)
    p_ij = softmax(z_i · z_j / student_temperature)
    L_i  = CE(q_i, p_i)
    """

    labels_bin = (labels > 0).to(z.dtype)
    batch_size = z.size(0)

    off_diag = ~torch.eye(batch_size, device=z.device, dtype=torch.bool)

    # [B, B] embedding similarity
    sim = torch.matmul(z, z.T)

    # [B, B] Jaccard label-set similarity
    and_counts = torch.matmul(labels_bin, labels_bin.T)
    or_counts = compute_or_counts(labels_bin, labels_bin).clamp_min(1.0)
    jaccard = and_counts / or_counts

    # Exclude self-pairs
    student_logits = sim / student_temperature
    student_logits = student_logits.masked_fill(~off_diag, float("-inf"))

    teacher_logits = jaccard / teacher_temperature
    teacher_logits = teacher_logits.masked_fill(~off_diag, float("-inf"))

    # Student distribution log p_ij
    log_prob = functional.log_softmax(student_logits, dim=1)

    # Teacher distribution q_ij
    with torch.no_grad():
        target_prob = functional.softmax(teacher_logits, dim=1)

    # Avoid 0 * -inf = nan on diagonal
    log_prob = log_prob.masked_fill(~off_diag, 0.0)
    target_prob = target_prob.masked_fill(~off_diag, 0.0)

    per_anchor = -(target_prob * log_prob).sum(dim=1)
    return per_anchor.mean()


class SoftJaccard(nn.Module):
    """Controlled Soft-Jaccard loss.

    This keeps the proposed soft-contrastive objective form, but replaces
    the proposed label-set similarity with Jaccard overlap.

    This is not the same as Base/JSCL:
    - Base: Jaccard is used as positive weight.
    - SoftJaccard: Jaccard is normalized into a soft teacher distribution.
    """

    def __init__(
        self,
        student_temperature: float = 0.1,
        teacher_temperature: float = 0.04,
    ) -> None:
        super().__init__()

        if student_temperature <= 0:
            raise ValueError("student_temperature must be > 0.")
        if teacher_temperature <= 0:
            raise ValueError("teacher_temperature must be > 0.")

        self.student_temperature = student_temperature
        self.teacher_temperature = teacher_temperature

    def forward(self, z: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
        """Compute the soft-Jaccard teacher cross-entropy objective."""
        batch_size = z.size(0)

        if batch_size < 2:
            raise RuntimeError("Contrastive learning requires batch_size >= 2.")

        if labels.ndim != 2 or labels.size(0) != batch_size:
            raise ValueError(
                f"labels must have shape [batch_size, num_labels], got {tuple(labels.shape)}"
            )

        normalized_z = functional.normalize(z, dim=1)

        return _compute_soft_jaccard_loss(
            z=normalized_z,
            labels=labels,
            student_temperature=self.student_temperature,
            teacher_temperature=self.teacher_temperature,
        )
