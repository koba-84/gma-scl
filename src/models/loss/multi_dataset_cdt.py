from __future__ import annotations

from pathlib import Path
from typing import cast

import torch
import torch.nn.functional as functional
from torch import nn

from src.models.loss.multi_dataset_mxclr import MultiDatasetMXCLR


def covariance_adjusted_scores(
    z: torch.Tensor,
    dataset_ids: torch.Tensor,
    domain_covariances: torch.Tensor,
) -> torch.Tensor:
    """Compute cosine scores within domains and covariance scores across domains."""
    if z.ndim != 2:
        raise ValueError(f"z must be [B, D], got {tuple(z.shape)}")
    if dataset_ids.ndim != 1 or dataset_ids.size(0) != z.size(0):
        raise ValueError(f"dataset_ids must be [{z.size(0)}], got {tuple(dataset_ids.shape)}")
    if domain_covariances.ndim != 3:
        raise ValueError(
            "domain_covariances must be [num_domains, D, D], "
            f"got {tuple(domain_covariances.shape)}"
        )
    if domain_covariances.size(1) != z.size(1) or domain_covariances.size(2) != z.size(1):
        raise ValueError(
            "domain_covariances must match z's embedding dimension, "
            f"got {tuple(domain_covariances.shape)} for z {tuple(z.shape)}"
        )
    ids = dataset_ids.to(device=z.device, dtype=torch.long)
    if torch.any(ids < 0) or torch.any(ids >= domain_covariances.size(0)):
        raise ValueError("dataset_ids contain an out-of-range value.")

    # CDT uses the covariance itself. Float32 keeps the quadratic form stable
    # when the trainer uses mixed precision for the encoder.
    features = functional.normalize(z.to(dtype=torch.float32), dim=1)
    covariances = domain_covariances.to(device=z.device, dtype=torch.float32)
    same_domain = ids[:, None] == ids[None, :]
    cosine_scores = features @ features.T
    cross_domain_scores = torch.zeros_like(cosine_scores)
    domain_indices = [torch.where(ids == domain_id)[0] for domain_id in range(covariances.size(0))]

    # AnInfoNCE uses a negative half quadratic form on normalized vectors.
    # The identity-metric case is exactly cosine minus one, so direct cosine
    # gives identical row-wise softmax probabilities without quadratic work.
    for anchor_domain in range(covariances.size(0)):
        anchor_indices = domain_indices[anchor_domain]
        if anchor_indices.numel() == 0:
            continue
        for candidate_domain in range(anchor_domain + 1, covariances.size(0)):
            candidate_indices = domain_indices[candidate_domain]
            if candidate_indices.numel() == 0:
                continue
            differences = (
                features[anchor_indices, None, :] - features[None, candidate_indices, :]
            ).reshape(-1, features.size(1))
            metric = 0.5 * (covariances[anchor_domain] + covariances[candidate_domain])
            quadratic = torch.einsum("pd,de,pe->p", differences, metric, differences)
            block = (-0.5 * quadratic).reshape(anchor_indices.numel(), candidate_indices.numel())
            cross_domain_scores[anchor_indices[:, None], candidate_indices[None, :]] = block
            cross_domain_scores[candidate_indices[:, None], anchor_indices[None, :]] = block.T

    return torch.where(same_domain, cosine_scores, cross_domain_scores)


class MultiDatasetCDT(nn.Module):
    """CDT-style covariance-aware MXCLR for mixed multi-dataset batches."""

    def __init__(
        self,
        num_domains: int = 3,
        embedding_dim: int = 128,
        instance_temperature: float = 0.1,
        graph_temperature: float = 0.01,
        label_embeddings: torch.Tensor | None = None,
        data_dir: str | Path | None = None,
        dataset_names: list[str] | tuple[str, ...] | None = None,
        sbert_model_name: str = "sentence-transformers/all-roberta-large-v1",
        sbert_max_length: int = 512,
        whitening: bool = False,
        label_weighting: str = "l2norm",
    ) -> None:
        super().__init__()
        if num_domains <= 0:
            raise ValueError("num_domains must be positive.")
        if embedding_dim <= 0:
            raise ValueError("embedding_dim must be positive.")
        if instance_temperature <= 0 or graph_temperature <= 0:
            raise ValueError("instance_temperature and graph_temperature must be > 0.")
        self.num_domains = int(num_domains)
        self.embedding_dim = int(embedding_dim)
        self.instance_temperature = float(instance_temperature)
        self.graph_temperature = float(graph_temperature)
        self.mxclr = MultiDatasetMXCLR(
            label_embeddings=label_embeddings,
            data_dir=data_dir,
            dataset_names=None if dataset_names is None else list(dataset_names),
            instance_temperature=instance_temperature,
            graph_temperature=graph_temperature,
            sbert_model_name=sbert_model_name,
            sbert_max_length=sbert_max_length,
            whitening=whitening,
            label_weighting=label_weighting,
        )
        self.register_buffer(
            "domain_covariances",
            torch.eye(self.embedding_dim).repeat(self.num_domains, 1, 1),
        )
        self.register_buffer("covariance_ready", torch.tensor(False, dtype=torch.bool))

    def set_domain_covariances(self, covariances: torch.Tensor) -> None:
        """Replace the detached per-dataset covariance state for the next epoch."""
        expected = (self.num_domains, self.embedding_dim, self.embedding_dim)
        if tuple(covariances.shape) != expected:
            raise ValueError(
                f"covariances must have shape {expected}, got {tuple(covariances.shape)}"
            )
        if not torch.isfinite(covariances).all():
            raise ValueError("covariances contain non-finite values.")
        domain_covariances = cast(torch.Tensor, self.domain_covariances)
        covariance_ready = cast(torch.Tensor, self.covariance_ready)
        detached = covariances.detach().to(
            device=domain_covariances.device,
            dtype=torch.float32,
        )
        detached = 0.5 * (detached + detached.transpose(-1, -2))
        with torch.no_grad():
            domain_covariances.copy_(detached)
            covariance_ready.fill_(True)

    def _validate_inputs(
        self,
        z: torch.Tensor,
        labels: torch.Tensor,
        dataset_ids: torch.Tensor,
    ) -> torch.Tensor:
        if z.ndim != 2 or z.size(1) != self.embedding_dim:
            raise ValueError(f"z must be [B, {self.embedding_dim}], got {tuple(z.shape)}")
        if labels.ndim != 2 or labels.size(0) != z.size(0):
            raise ValueError(
                f"labels must be [B, L] with B={z.size(0)}, got {tuple(labels.shape)}"
            )
        if dataset_ids.ndim != 1 or dataset_ids.size(0) != z.size(0):
            raise ValueError(f"dataset_ids must be [{z.size(0)}], got {tuple(dataset_ids.shape)}")
        ids = dataset_ids.to(device=z.device, dtype=torch.long)
        if torch.any(ids < 0) or torch.any(ids >= self.num_domains):
            raise ValueError("dataset_ids contain an out-of-range value.")
        covariance_ready = cast(torch.Tensor, self.covariance_ready)
        if not bool(covariance_ready.item()):
            raise RuntimeError("CDT domain covariances are not initialized.")
        if z.size(0) < 2:
            raise RuntimeError("Multi-dataset CDT requires batch_size >= 2.")
        return ids

    def forward(
        self,
        z: torch.Tensor,
        labels: torch.Tensor,
        dataset_ids: torch.Tensor,
    ) -> torch.Tensor:
        """Compute covariance-aware model logits against the semantic target graph."""
        ids = self._validate_inputs(z, labels, dataset_ids)
        scores = covariance_adjusted_scores(
            z,
            ids,
            cast(torch.Tensor, self.domain_covariances),
        )
        batch_size = z.size(0)
        off_diagonal = ~torch.eye(batch_size, device=z.device, dtype=torch.bool)
        model_logits = scores / self.instance_temperature
        model_logits = model_logits.masked_fill(~off_diagonal, float("-inf"))
        log_prob = functional.log_softmax(model_logits, dim=1)

        graph = self.mxclr.score_graph(labels).to(device=z.device, dtype=torch.float32)
        graph_logits = graph / self.graph_temperature
        graph_logits = graph_logits.masked_fill(~off_diagonal, float("-inf"))
        target = functional.softmax(graph_logits, dim=1)
        return (
            -(target.masked_fill(~off_diagonal, 0.0) * log_prob.masked_fill(~off_diagonal, 0.0))
            .sum(dim=1)
            .mean()
        )


__all__ = ["MultiDatasetCDT", "covariance_adjusted_scores"]
