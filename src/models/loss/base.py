from __future__ import annotations

import torch
import torch.nn.functional as functional
from torch import nn

from src.models.loss.components.label_overlap import compute_or_counts


def _compute_base_loss(
    z: torch.Tensor,
    labels: torch.Tensor,
    *,
    temperature: float,
    eps: float,
) -> torch.Tensor:
    labels_bin = (labels > 0).to(z.dtype)
    batch_size = z.size(0)

    sim = torch.matmul(z, z.T)
    off_diag = ~torch.eye(batch_size, device=z.device, dtype=torch.bool)

    mask_and = torch.matmul(labels_bin, labels_bin.T) * off_diag.to(z.dtype)
    mask_or = compute_or_counts(labels_bin, labels_bin).clamp_min(1.0)
    pos_weights = (mask_and / mask_or).to(z.dtype)

    logits = sim / temperature
    logits = logits.masked_fill(~off_diag, float("-inf"))
    log_prob = logits - torch.logsumexp(logits, dim=1, keepdim=True)

    weighted_log_prob = torch.where(pos_weights > 0, log_prob, torch.zeros_like(log_prob))
    pos_weight_sum = pos_weights.sum(dim=1)
    per_anchor = -(pos_weights * weighted_log_prob).sum(dim=1) / pos_weight_sum.clamp_min(eps)

    valid = pos_weight_sum > 0
    if not torch.any(valid):
        return z.sum() * 0.0
    return per_anchor[valid].mean()


class Base(nn.Module):
    """Multi-label contrastive base loss adapted from supcon.

    Uses weighted supervised contrastive objective where positive weights are Jaccard(label_i,
    label_j) and self-pairs are excluded.
    """

    def __init__(self, temperature: float = 0.07, eps: float = 1e-8) -> None:
        super().__init__()
        if temperature <= 0:
            raise ValueError("temperature must be > 0.")
        self.temperature = temperature
        self.eps = eps

    def forward(self, z: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
        """Run the forward computation and return model outputs."""
        batch_size = z.size(0)
        if batch_size < 2:
            raise RuntimeError("Contrastive learning requires batch_size >= 2.")
        if labels.ndim != 2 or labels.size(0) != batch_size:
            raise ValueError(
                f"labels must have shape [batch_size, num_labels], got {tuple(labels.shape)}"
            )

        normalized_z = functional.normalize(z, dim=1)
        return _compute_base_loss(
            z=normalized_z,
            labels=labels,
            temperature=self.temperature,
            eps=self.eps,
        )
