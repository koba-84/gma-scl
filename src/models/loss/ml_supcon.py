from __future__ import annotations

import torch
import torch.nn.functional as functional
from torch import nn


def _compute_ml_supcon_loss(
    z: torch.Tensor,
    labels: torch.Tensor,
    *,
    temperature: float,
    eps: float,
) -> torch.Tensor:
    labels_bin = labels > 0
    batch_size = z.size(0)
    sample_indices, label_indices = torch.where(labels_bin)
    if sample_indices.numel() == 0:
        return z.new_tensor(0.0)

    logits = torch.matmul(z, z.T) / temperature
    expanded_logits = logits.index_select(0, sample_indices)
    positive_mask = labels_bin[:, label_indices].T

    self_mask = torch.ones(
        (sample_indices.numel(), batch_size),
        device=z.device,
        dtype=torch.bool,
    )
    self_mask[torch.arange(sample_indices.numel(), device=z.device), sample_indices] = False

    positive_mask = positive_mask & self_mask
    expanded_logits = expanded_logits.masked_fill(~self_mask, float("-inf"))
    log_prob = expanded_logits - torch.logsumexp(expanded_logits, dim=1, keepdim=True)

    pos_counts = positive_mask.sum(dim=1).to(z.dtype)
    positive_log_prob = torch.where(
        positive_mask,
        log_prob,
        torch.zeros_like(log_prob),
    )
    per_row = -positive_log_prob.sum(dim=1) / pos_counts.clamp_min(eps)
    return per_row.mean()


class MulSupCon(nn.Module):
    """Label-wise supervised contrastive loss for single-view multi-label batches."""

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
        return _compute_ml_supcon_loss(
            z=normalized_z,
            labels=labels,
            temperature=self.temperature,
            eps=self.eps,
        )
