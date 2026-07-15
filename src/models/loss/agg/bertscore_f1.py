from __future__ import annotations

import torch
import torch.nn.functional as functional
from torch import nn


def _build_similarity_matrix(
    label_embeddings: torch.Tensor,
    *,
    npmi: torch.Tensor,
    transport_lambda: float,
) -> torch.Tensor:
    if label_embeddings.ndim != 2:
        raise ValueError(f"embeddings must be [L, D], got {tuple(label_embeddings.shape)}")
    norms = label_embeddings.norm(dim=1)
    if not torch.isfinite(norms).all():
        raise ValueError("Label embeddings contain non-finite norms.")
    if torch.any(norms <= 0):
        raise ValueError("Label embeddings must have strictly positive norms.")
    normalized = functional.normalize(label_embeddings.to(dtype=torch.float32), dim=1)
    semantic_similarity = normalized @ normalized.T
    if not torch.isfinite(semantic_similarity).all():
        raise ValueError("Semantic label similarity contains non-finite values.")
    statistic_component = npmi.to(
        device=semantic_similarity.device,
        dtype=semantic_similarity.dtype,
    )
    similarity_matrix = (
        ((1.0 - transport_lambda) * semantic_similarity)
        + (transport_lambda * statistic_component)
        + 1.0
    ) / 2.0
    return similarity_matrix


def _compute_directional_score(
    labels_bin: torch.Tensor,
    *,
    similarity_matrix: torch.Tensor,
    label_weights: torch.Tensor,
) -> torch.Tensor:
    label_mask = labels_bin > 0
    has_label = label_mask.any(dim=1, keepdim=True)
    best_to_target = similarity_matrix.unsqueeze(0).expand(labels_bin.size(0), -1, -1)
    best_to_target = best_to_target.masked_fill(~label_mask.unsqueeze(1), float("-inf"))
    best_to_target = best_to_target.max(dim=2).values
    best_to_target = torch.where(has_label, best_to_target, torch.zeros_like(best_to_target))
    if label_weights.ndim != 1 or label_weights.size(0) != labels_bin.size(1):
        raise ValueError(
            f"label_weights must be [L], got {tuple(label_weights.shape)} "
            f"for L={labels_bin.size(1)}."
        )
    source_weights = (labels_bin * label_weights.unsqueeze(0)).to(labels_bin.dtype)
    denom = source_weights.sum(dim=1).clamp_min(1.0)
    return (source_weights @ best_to_target.T) / denom[:, None]


class _BaseBERTScoreGraph(nn.Module):
    """Build MXCLR score graphs with BERTScore-style directional aggregation."""

    @staticmethod
    def required_label_stats() -> frozenset[str]:
        """Return the train.csv-derived label statistics required by this agg."""
        return frozenset({"npmi", "label_idf"})

    def __init__(
        self,
        eps: float = 1e-8,
        transport_lambda: float = 5e-1,
    ) -> None:
        super().__init__()
        self.eps = eps
        self.transport_lambda = transport_lambda

    def forward(
        self,
        labels_bin: torch.Tensor,
        label_embeddings: torch.Tensor,
        *,
        npmi: torch.Tensor,
        label_idf: torch.Tensor,
    ) -> torch.Tensor:
        """Return the directional MXCLR pairwise score matrix for BERTScore-style aggs."""
        similarity_matrix = _build_similarity_matrix(
            label_embeddings,
            npmi=npmi,
            transport_lambda=self.transport_lambda,
        )
        return _compute_directional_score(
            labels_bin,
            similarity_matrix=similarity_matrix,
            label_weights=label_idf,
        )


class BERTScorePrecisionGraph(_BaseBERTScoreGraph):
    """Build MXCLR score graphs with BERTScore-style precision aggregation."""

    def forward(
        self,
        labels_bin: torch.Tensor,
        label_embeddings: torch.Tensor,
        *,
        npmi: torch.Tensor,
        label_idf: torch.Tensor,
    ) -> torch.Tensor:
        """Return the MXCLR pairwise score matrix for BERTScore-style precision."""
        return (
            super()
            .forward(
                labels_bin,
                label_embeddings,
                npmi=npmi,
                label_idf=label_idf,
            )
            .clamp(0.0, 1.0)
        )


class BERTScoreRecallGraph(_BaseBERTScoreGraph):
    """Build MXCLR score graphs with BERTScore-style recall aggregation."""

    def forward(
        self,
        labels_bin: torch.Tensor,
        label_embeddings: torch.Tensor,
        *,
        npmi: torch.Tensor,
        label_idf: torch.Tensor,
    ) -> torch.Tensor:
        """Return the MXCLR pairwise score matrix for BERTScore-style recall."""
        return (
            super()
            .forward(
                labels_bin,
                label_embeddings,
                npmi=npmi,
                label_idf=label_idf,
            )
            .T.clamp(0.0, 1.0)
        )


class BERTScoreF1Graph(_BaseBERTScoreGraph):
    """Build MXCLR score graphs with BERTScore-style F1 aggregation."""

    def forward(
        self,
        labels_bin: torch.Tensor,
        label_embeddings: torch.Tensor,
        *,
        npmi: torch.Tensor,
        label_idf: torch.Tensor,
    ) -> torch.Tensor:
        """Return the MXCLR pairwise score matrix for BERTScore-style F1 aggregation."""
        precision = super().forward(
            labels_bin,
            label_embeddings,
            npmi=npmi,
            label_idf=label_idf,
        )
        recall = precision.T
        f1 = (2.0 * precision * recall) / (precision + recall).clamp_min(self.eps)
        f1 = torch.where(
            (precision > 0) | (recall > 0),
            f1,
            torch.zeros_like(f1),
        )
        return f1.clamp(0.0, 1.0)


class BERTScoreUniformF1Graph(_BaseBERTScoreGraph):
    """Build MXCLR score graphs with equal-label-weight BERTScore-style F1."""

    @staticmethod
    def required_label_stats() -> frozenset[str]:
        """Return the train.csv-derived label statistics required by this agg."""
        return frozenset({"npmi"})

    def forward(
        self,
        labels_bin: torch.Tensor,
        label_embeddings: torch.Tensor,
        *,
        npmi: torch.Tensor,
        label_idf: torch.Tensor | None = None,
    ) -> torch.Tensor:
        """Return the MXCLR pairwise score matrix for uniform BERTScore-style F1."""
        similarity_matrix = _build_similarity_matrix(
            label_embeddings,
            npmi=npmi,
            transport_lambda=self.transport_lambda,
        )
        label_weights = torch.ones(
            labels_bin.size(1),
            device=labels_bin.device,
            dtype=labels_bin.dtype,
        )
        precision = _compute_directional_score(
            labels_bin,
            similarity_matrix=similarity_matrix,
            label_weights=label_weights,
        )
        recall = precision.T
        f1 = (2.0 * precision * recall) / (precision + recall).clamp_min(self.eps)
        f1 = torch.where(
            (precision > 0) | (recall > 0),
            f1,
            torch.zeros_like(f1),
        )
        return f1.clamp(0.0, 1.0)
