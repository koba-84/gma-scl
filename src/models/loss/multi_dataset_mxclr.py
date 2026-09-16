from __future__ import annotations

import json
from pathlib import Path
from typing import cast

import torch
import torch.nn.functional as functional
from torch import nn


def _load_label_descriptions(path: str | Path) -> list[str]:
    label_path = Path(path)
    if not label_path.is_file():
        raise FileNotFoundError(f"Label description file not found: {label_path}")
    payload = json.loads(label_path.read_text(encoding="utf-8"))
    labels = payload.get("labels")
    if not isinstance(labels, list) or not labels:
        raise ValueError("Invalid label description file: 'labels' must be a non-empty list.")
    rows = sorted(labels, key=lambda row: int(row["index"]))
    descriptions = [str(row.get("description", "")).strip() for row in rows]
    if any(not description for description in descriptions):
        raise ValueError("All labels must have non-empty descriptions.")
    return descriptions


def _whiten_label_embeddings(embeddings: torch.Tensor) -> torch.Tensor:
    if embeddings.ndim != 2:
        raise ValueError(f"label embeddings must be [L, D], got {tuple(embeddings.shape)}")
    centered = embeddings - embeddings.mean(dim=0, keepdim=True)
    covariance = centered.T @ centered / centered.size(0)
    eigenvalues, eigenvectors = torch.linalg.eigh(covariance)
    scales = torch.rsqrt(eigenvalues.clamp_min(1e-8))
    return centered @ (eigenvectors @ torch.diag(scales) @ eigenvectors.T)


def build_semantic_graph(
    labels: torch.Tensor,
    label_embeddings: torch.Tensor,
) -> torch.Tensor:
    """Build an L2-norm weighted label-embedding-only graph for a mixed batch.

    ``labels`` uses a disjoint global label space. Dataset-specific local labels
    are mapped to this space by the multi-dataset datamodule before collation.
    """
    if labels.ndim != 2:
        raise ValueError(f"labels must be [N, L], got {tuple(labels.shape)}")
    if label_embeddings.ndim != 2 or label_embeddings.size(0) != labels.size(1):
        raise ValueError(
            "label_embeddings must have shape [L, D] matching labels, "
            f"got {tuple(label_embeddings.shape)} for labels {tuple(labels.shape)}"
        )
    raw_embeddings = label_embeddings.to(torch.float32)
    if not torch.isfinite(raw_embeddings).all():
        raise ValueError("Label embeddings contain non-finite values.")
    label_weights = raw_embeddings.norm(dim=1).clamp_min(1e-8)
    normalized_embeddings = functional.normalize(raw_embeddings, dim=1)
    label_similarities = (normalized_embeddings @ normalized_embeddings.T).clamp(0.0, 1.0)
    active = labels > 0
    active_float = active.to(dtype=torch.float32)
    weighted_active = active_float * label_weights.unsqueeze(0)
    label_weight_sums = weighted_active.sum(dim=1)
    nonempty = active_float.any(dim=1)

    # max_to_label[source, target_label] is the maximum label similarity from
    # any active source label to target_label. The masked reduction keeps the
    # work proportional to N*L*L and avoids a Python loop over sample pairs.
    max_to_label = (
        label_similarities.unsqueeze(0)
        .masked_fill(
            ~active.unsqueeze(-1),
            float("-inf"),
        )
        .amax(dim=1)
    )
    max_to_label = max_to_label.masked_fill(~nonempty.unsqueeze(1), 0.0)

    precision = (max_to_label @ weighted_active.T) / label_weight_sums.clamp_min(1e-8).unsqueeze(0)
    recall = (weighted_active @ max_to_label.T) / label_weight_sums.clamp_min(1e-8).unsqueeze(1)
    denominator = precision + recall
    graph = torch.where(
        denominator > 0,
        2.0 * precision * recall / denominator,
        torch.zeros_like(denominator),
    )
    graph = graph.masked_fill(~(nonempty.unsqueeze(1) & nonempty.unsqueeze(0)), 0.0)
    graph.fill_diagonal_(0.0)
    if not torch.isfinite(graph).all():
        raise ValueError("Semantic graph contains non-finite values.")
    return graph.clamp(0.0, 1.0)


def _compute_mxclr_loss(
    z: torch.Tensor,
    graph: torch.Tensor,
    *,
    instance_temperature: float,
    graph_temperature: float,
) -> torch.Tensor:
    batch_size = z.size(0)
    off_diagonal = ~torch.eye(batch_size, device=z.device, dtype=torch.bool)
    instance_logits = (z @ z.T) / instance_temperature
    instance_logits = instance_logits.masked_fill(~off_diagonal, float("-inf"))
    log_prob = functional.log_softmax(instance_logits, dim=1)

    graph_logits = graph.to(dtype=z.dtype) / graph_temperature
    graph_logits = graph_logits.masked_fill(~off_diagonal, float("-inf"))
    target = functional.softmax(graph_logits, dim=1)
    return (
        -(target.masked_fill(~off_diagonal, 0.0) * log_prob.masked_fill(~off_diagonal, 0.0))
        .sum(dim=1)
        .mean()
    )


class MultiDatasetMXCLR(nn.Module):
    """MXCLR using L2-norm weighted semantic label embeddings across datasets."""

    def __init__(
        self,
        label_embeddings: torch.Tensor | None = None,
        instance_temperature: float = 0.07,
        graph_temperature: float = 0.1,
        data_dir: str | Path | None = None,
        dataset_names: list[str] | None = None,
        sbert_model_name: str = "sentence-transformers/all-roberta-large-v1",
        sbert_max_length: int = 512,
        whitening: bool = False,
        label_weighting: str = "l2norm",
    ) -> None:
        super().__init__()
        if label_embeddings is None:
            if data_dir is None or not dataset_names:
                raise ValueError("label_embeddings or data_dir with dataset_names is required.")
            built = type(self).from_dataset_descriptions(
                data_dir=data_dir,
                dataset_names=dataset_names,
                model_name=sbert_model_name,
                max_length=sbert_max_length,
                instance_temperature=instance_temperature,
                graph_temperature=graph_temperature,
                whitening=whitening,
                label_weighting=label_weighting,
            )
            label_embeddings = cast(torch.Tensor, built.label_embeddings).detach().cpu()
        if label_embeddings.ndim != 2 or label_embeddings.size(0) == 0:
            raise ValueError("label_embeddings must be a non-empty [L, D] tensor.")
        if instance_temperature <= 0 or graph_temperature <= 0:
            raise ValueError("instance_temperature and graph_temperature must be > 0.")
        if label_weighting != "l2norm":
            raise ValueError("MultiDatasetMXCLR supports only label_weighting='l2norm'.")
        self.instance_temperature = float(instance_temperature)
        self.graph_temperature = float(graph_temperature)
        self.label_weighting = label_weighting
        self.register_buffer("label_embeddings", label_embeddings.to(dtype=torch.float32))

    @staticmethod
    def encode_label_descriptions(
        descriptions: list[str],
        model_name: str,
        max_length: int,
        whitening: bool = False,
    ) -> torch.Tensor:
        """Encode label descriptions with the configured SentenceTransformer."""
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise ImportError(
                "sentence-transformers is required for MXCLR semantic initialization."
            ) from exc
        model = SentenceTransformer(model_name)
        model.max_seq_length = max_length
        embeddings = model.encode(
            descriptions,
            convert_to_tensor=True,
            normalize_embeddings=False,
        )
        tensor = (
            embeddings if isinstance(embeddings, torch.Tensor) else torch.as_tensor(embeddings)
        )
        tensor = tensor.to(dtype=torch.float32, device="cpu")
        return _whiten_label_embeddings(tensor) if whitening else tensor

    @classmethod
    def from_dataset_descriptions(
        cls,
        data_dir: str | Path,
        dataset_names: list[str],
        model_name: str,
        max_length: int,
        instance_temperature: float = 0.07,
        graph_temperature: float = 0.1,
        whitening: bool = False,
        label_weighting: str = "l2norm",
    ) -> MultiDatasetMXCLR:
        """Build a loss from ordered per-dataset label description files."""
        embeddings: list[torch.Tensor] = []
        for dataset_name in dataset_names:
            path = Path(data_dir) / dataset_name / "label_descriptions.json"
            descriptions = _load_label_descriptions(path)
            embeddings.append(
                cls.encode_label_descriptions(
                    descriptions,
                    model_name=model_name,
                    max_length=max_length,
                    whitening=whitening,
                )
            )
        dimensions = {int(embedding.size(1)) for embedding in embeddings}
        if len(dimensions) != 1:
            raise ValueError("All dataset label embeddings must have the same dimension.")
        return cls(
            torch.cat(embeddings, dim=0),
            instance_temperature=instance_temperature,
            graph_temperature=graph_temperature,
            label_weighting=label_weighting,
        )

    def score_graph(self, labels: torch.Tensor) -> torch.Tensor:
        """Return the L2-norm weighted semantic graph for a global-label batch."""
        label_embeddings = cast(torch.Tensor, self.label_embeddings)
        return build_semantic_graph(labels, label_embeddings)

    def forward(self, z: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
        """Compute the MXCLR soft-target objective for a mixed batch."""
        if z.ndim != 2:
            raise ValueError(f"z must be [N, D], got {tuple(z.shape)}")
        if labels.ndim != 2 or labels.size(0) != z.size(0):
            raise ValueError(
                f"labels must be [N, L] with N={z.size(0)}, got {tuple(labels.shape)}"
            )
        if z.size(0) < 2:
            raise RuntimeError("Multi-dataset MXCLR requires batch_size >= 2.")
        label_embeddings = cast(torch.Tensor, self.label_embeddings)
        if labels.size(1) != label_embeddings.size(0):
            raise ValueError("labels and label_embeddings must have the same label dimension.")
        normalized_z = functional.normalize(z, dim=1)
        graph = self.score_graph(labels).to(device=z.device)
        return _compute_mxclr_loss(
            normalized_z,
            graph,
            instance_temperature=self.instance_temperature,
            graph_temperature=self.graph_temperature,
        )
