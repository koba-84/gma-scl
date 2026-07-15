from __future__ import annotations

import json
from pathlib import Path

import torch
import torch.nn.functional as functional
from torch import nn

from src.models.loss.components.label_stats import (
    compute_frequency,
    compute_idf,
    compute_npmi,
)

_NUMERICAL_STABILITY_EPS = 1e-8


def _load_label_descriptions(path: str | Path) -> list[str]:
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Label description file not found: {p}")

    payload = json.loads(p.read_text(encoding="utf-8"))
    labels = payload.get("labels")
    if not isinstance(labels, list) or not labels:
        raise ValueError("Invalid label description file: 'labels' must be a non-empty list.")

    sorted_rows = sorted(labels, key=lambda row: int(row["index"]))
    descriptions = [str(row.get("description", "")).strip() for row in sorted_rows]
    if any(not description for description in descriptions):
        raise ValueError("All labels must have non-empty descriptions.")
    return descriptions


def _resolve_label_description_path(data_dir: str | Path, dataset_name: str) -> Path:
    return Path(data_dir) / dataset_name / "label_descriptions.json"


def _required_label_stats(agg: nn.Module) -> frozenset[str]:
    getter = getattr(agg, "required_label_stats", None)
    if getter is None:
        return frozenset()
    stats = getter()
    if not isinstance(stats, frozenset):
        stats = frozenset(stats)
    invalid = stats.difference({"npmi", "label_idf", "label_frequency"})
    if invalid:
        raise ValueError(f"agg requested unsupported label stats: {sorted(invalid)}")
    return stats


def _whiten_label_embeddings(embeddings: torch.Tensor) -> torch.Tensor:
    if embeddings.ndim != 2:
        raise ValueError(f"label embeddings must be [L, D], got {tuple(embeddings.shape)}")
    centered = embeddings - embeddings.mean(dim=0, keepdim=True)
    covariance = centered.T @ centered / centered.size(0)
    eigenvalues, eigenvectors = torch.linalg.eigh(covariance)
    scales = torch.rsqrt(eigenvalues.clamp_min(_NUMERICAL_STABILITY_EPS))
    whitening_matrix = eigenvectors @ torch.diag(scales) @ eigenvectors.T
    return centered @ whitening_matrix


def _compute_mxclr_loss(
    z: torch.Tensor,
    g_soft: torch.Tensor,
    *,
    instance_temperature: float,
    graph_temperature: float,
) -> torch.Tensor:
    n = z.size(0)

    logits = (z @ z.T) / instance_temperature

    off_diag = ~torch.eye(n, device=z.device, dtype=torch.bool)
    logits = logits.masked_fill(~off_diag, float("-inf"))
    log_p = nn.functional.log_softmax(logits, dim=1)

    s_logits = g_soft.to(z.dtype) / graph_temperature
    s_logits = s_logits.masked_fill(~off_diag, float("-inf"))
    s = nn.functional.softmax(s_logits, dim=1)

    loss_per_i = -(s.masked_fill(~off_diag, 0.0) * log_p.masked_fill(~off_diag, 0.0)).sum(dim=1)
    return loss_per_i.mean()


class MXCLR(nn.Module):
    """X-Sample Contrastive Loss (X-CLR)."""

    def __init__(
        self,
        data_dir: str,
        instance_temperature: float = 0.07,
        graph_temperature: float = 0.1,
        dataset_name: str = "aapd",
        sbert_model_name: str = "sentence-transformers/all-roberta-large-v1",
        sbert_max_length: int = 512,
        whitening: bool = False,
        agg: nn.Module | None = None,
    ) -> None:
        super().__init__()
        if instance_temperature <= 0 or graph_temperature <= 0:
            raise ValueError("instance_temperature and graph_temperature must be > 0.")
        if sbert_max_length <= 0:
            raise ValueError("sbert_max_length must be > 0.")
        self.instance_temperature = instance_temperature
        self.graph_temperature = graph_temperature
        self.data_dir = data_dir
        self.sbert_max_length = sbert_max_length
        self.agg = agg
        self.dataset_name = dataset_name.lower()
        self.register_buffer("label_embeddings", torch.empty(0), persistent=True)
        self.register_buffer("label_npmi", torch.empty(0), persistent=True)
        self.register_buffer("label_idf", torch.empty(0), persistent=True)
        self.register_buffer("label_frequency", torch.empty(0), persistent=True)

        if agg is None:
            raise ValueError("agg is required for MXCLR initialization.")
        self.label_embeddings = self._build_label_embeddings(
            data_dir=self.data_dir,
            dataset_name=self.dataset_name,
            sbert_model_name=sbert_model_name,
            sbert_max_length=sbert_max_length,
            whitening=whitening,
        )
        required_stats = _required_label_stats(agg)
        if "npmi" in required_stats:
            self.label_npmi = compute_npmi(
                data_dir=self.data_dir,
                dataset_name=self.dataset_name,
            ).to(dtype=torch.float32, device="cpu")
        if "label_idf" in required_stats:
            self.label_idf = compute_idf(
                data_dir=self.data_dir,
                dataset_name=self.dataset_name,
            ).to(dtype=torch.float32, device="cpu")
        if "label_frequency" in required_stats:
            self.label_frequency = compute_frequency(
                data_dir=self.data_dir,
                dataset_name=self.dataset_name,
            ).to(dtype=torch.float32, device="cpu")

    @staticmethod
    def _encode_descriptions_with_sbert(
        descriptions: list[str],
        model_name: str,
        max_length: int,
    ) -> torch.Tensor:
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
            normalize_embeddings=True,
        )
        if not isinstance(embeddings, torch.Tensor):
            embeddings = torch.as_tensor(embeddings, dtype=torch.float32)
        return embeddings.to(dtype=torch.float32, device="cpu")

    @staticmethod
    def _build_label_embeddings(
        data_dir: str | Path,
        dataset_name: str,
        sbert_model_name: str,
        sbert_max_length: int,
        whitening: bool = False,
    ) -> torch.Tensor:
        descriptions = _load_label_descriptions(
            _resolve_label_description_path(data_dir=data_dir, dataset_name=dataset_name)
        )
        embeddings = MXCLR._encode_descriptions_with_sbert(
            descriptions,
            sbert_model_name,
            sbert_max_length,
        )
        if not whitening:
            return embeddings
        return _whiten_label_embeddings(embeddings)

    def score_graph(self, labels: torch.Tensor) -> torch.Tensor:
        """Build a soft [N, N] score graph from multi-label targets."""
        if labels.ndim != 2:
            raise ValueError(f"labels must be [N, L], got {tuple(labels.shape)}")
        x = (labels > 0).to(torch.float32)

        if self.label_embeddings.numel() == 0:
            raise RuntimeError("label_embeddings is not initialized.")
        l = x.size(1)
        if self.label_embeddings.ndim != 2 or self.label_embeddings.size(0) != l:
            raise ValueError(
                "Label dimension mismatch: "
                f"labels have L={l}, label embeddings are {tuple(self.label_embeddings.shape)}."
            )
        agg = self.agg
        if agg is None:
            raise RuntimeError("agg is not initialized.")
        required_stats = _required_label_stats(agg)
        agg_kwargs: dict[str, torch.Tensor] = {}
        if "npmi" in required_stats:
            if self.label_npmi.numel() == 0:
                raise RuntimeError("npmi is not initialized.")
            agg_kwargs["npmi"] = self.label_npmi
        if "label_idf" in required_stats:
            if self.label_idf.numel() == 0:
                raise RuntimeError("label_idf is not initialized.")
            agg_kwargs["label_idf"] = self.label_idf
        if "label_frequency" in required_stats:
            if self.label_frequency.numel() == 0:
                raise RuntimeError("label_frequency is not initialized.")
            agg_kwargs["label_frequency"] = self.label_frequency
        return agg(
            labels_bin=x,
            label_embeddings=self.label_embeddings,
            **agg_kwargs,
        )

    def forward(self, z: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """Run the forward computation and return model outputs."""
        if z.ndim != 2:
            raise ValueError(f"z must be [N, D], got {tuple(z.shape)}")
        n = z.size(0)
        if n < 2:
            raise RuntimeError("X-CLR requires batch_size >= 2.")
        if target.ndim != 2 or target.size(0) != n:
            raise ValueError(
                f"target must be [N, L] or [N, N] with N={n}, got {tuple(target.shape)}"
            )
        normalized_z = functional.normalize(z, dim=1)

        if target.shape == (n, n):
            g_soft = target
        else:
            g_soft = self.score_graph(target)
        return _compute_mxclr_loss(
            z=normalized_z,
            g_soft=g_soft,
            instance_temperature=self.instance_temperature,
            graph_temperature=self.graph_temperature,
        )
