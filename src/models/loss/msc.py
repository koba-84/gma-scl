from __future__ import annotations

import torch
import torch.nn.functional as functional
from torch import Tensor, nn

from src.models.loss.components.label_overlap import compute_or_counts

EPS = 1e-8


def _log_softmax_with_temperature(matrix: Tensor, temperature: float, mask: Tensor) -> Tensor:
    if temperature <= 0:
        raise ValueError("temperature must be > 0.")
    scaled_matrix = matrix / temperature
    max_columns = torch.max(scaled_matrix, dim=1, keepdim=True)[0]
    logits = scaled_matrix - max_columns.detach()
    exp_logits = torch.exp(logits)
    denom = (exp_logits * mask).sum(dim=1, keepdim=True).clamp_min(EPS)
    return logits - torch.log(denom)


def _compute_msc_loss(
    output_features: Tensor,
    labels_query: Tensor,
    prototype_features: Tensor,
    alpha: float,
    beta: float,
    temperature: float,
) -> Tensor:
    total = labels_query.size(0)
    nb_labels = prototype_features.size(0)

    mask_and_features = torch.einsum("ac,bc->abc", labels_query, labels_query)
    mask_or_features = compute_or_counts(query_tensor=labels_query, key_tensor=labels_query)
    mask_or_features = mask_or_features.unsqueeze(2).clamp_min(1.0)
    mask_and_features = mask_and_features * (1 / mask_or_features) * alpha

    normalize = mask_and_features.sum(dim=1)

    labels_per_sample = labels_query.sum(dim=1, keepdim=True).clamp_min(1.0)
    normalize = normalize + (-alpha / labels_per_sample + 1) * labels_query

    denom = normalize.unsqueeze(1) + EPS
    w_features_features = (mask_and_features / denom).sum(dim=2)

    parts_features = [output_features @ output_features.T]
    parts_weights = [w_features_features]
    section_lengths = [total]

    w_features_proto = labels_query / (normalize + EPS)
    parts_features.append(output_features @ prototype_features.T)
    parts_weights.append(w_features_proto)
    section_lengths.append(nb_labels)

    total_refs = sum(section_lengths)
    mask_diagonal = output_features.new_ones((total, total_refs))
    if total > 0:
        indices = torch.arange(total, device=mask_diagonal.device)
        mask_diagonal[indices, indices] = 0

    w = torch.cat(parts_weights, dim=1) * mask_diagonal
    final_features = torch.cat(parts_features, dim=1)

    normalize_mask = output_features.new_full((total_refs,), beta)
    normalize_mask[total_refs - nb_labels :] = 1

    log_softmax = _log_softmax_with_temperature(
        matrix=final_features,
        temperature=temperature,
        mask=mask_diagonal * normalize_mask.unsqueeze(0),
    )
    return -(log_softmax * w).sum(dim=1)


class MSC(nn.Module):
    """Multi-label contrastive loss with optional prototype/key/queue inputs.

    Standard training path is `forward(z, labels, prototype=...)`.
    """

    def __init__(self, alpha: float = 1.0, beta: float = 1.0, temperature: float = 0.07) -> None:
        super().__init__()
        if temperature <= 0:
            raise ValueError("temperature must be > 0.")
        self.alpha = alpha
        self.beta = beta
        self.temperature = temperature

    def forward(
        self,
        z: Tensor,
        labels: Tensor,
        prototype: Tensor | None = None,
    ) -> Tensor:
        """Run the forward computation and return model outputs."""
        if z.ndim != 2:
            raise ValueError(f"z must be [batch_size, dim], got {tuple(z.shape)}")
        if labels.ndim != 2 or labels.size(0) != z.size(0):
            raise ValueError(
                f"labels must have shape [batch_size, num_labels], got {tuple(labels.shape)}"
            )
        if prototype is None:
            raise ValueError("prototype is required for MSC.")
        if prototype.ndim != 2:
            raise ValueError(
                f"prototype must have shape [num_labels, dim], got {tuple(prototype.shape)}"
            )
        if z.size(0) < 2:
            raise RuntimeError("Contrastive learning requires batch_size >= 2.")

        normalized_z = functional.normalize(z, dim=1)
        labels_query = (labels > 0).to(normalized_z.dtype)
        prototype_features = prototype.to(z.dtype)

        loss_per_sample = _compute_msc_loss(
            output_features=normalized_z,
            labels_query=labels_query,
            prototype_features=prototype_features,
            alpha=self.alpha,
            beta=self.beta,
            temperature=self.temperature,
        )
        labels_per_sample = labels_query.sum(dim=1).clamp_min(1.0)
        return (loss_per_sample / (labels_per_sample + EPS)).mean()
