from __future__ import annotations

import torch
import torch.nn.functional as functional
from torch import nn

from src.models.loss.components.listmle import compute_listmle_loss
from src.models.loss.mxclr import MXCLR, _compute_mxclr_loss


def _compute_mxclr_rank_loss(
    z: torch.Tensor,
    g_soft: torch.Tensor,
    *,
    instance_temperature: float,
    graph_temperature: float,
    rank_temperature: float,
    lambda_rank: float,
) -> torch.Tensor:
    mxclr_loss = _compute_mxclr_loss(
        z=z,
        g_soft=g_soft,
        instance_temperature=instance_temperature,
        graph_temperature=graph_temperature,
    )
    if lambda_rank == 0.0:
        return mxclr_loss

    off_diag = ~torch.eye(z.size(0), device=z.device, dtype=torch.bool)
    student_scores = (z @ z.T) / rank_temperature
    rank_loss = compute_listmle_loss(
        student_scores=student_scores,
        teacher_scores=g_soft.to(dtype=z.dtype, device=z.device),
        valid_mask=off_diag,
    )
    return mxclr_loss + (lambda_rank * rank_loss)


class MXCLRRank(MXCLR):
    """MXCLR with an auxiliary teacher-order ListMLE term."""

    def __init__(
        self,
        data_dir: str,
        instance_temperature: float = 0.1,
        graph_temperature: float = 0.1,
        rank_temperature: float = 0.1,
        lambda_rank: float = 0.5,
        dataset_name: str = "aapd",
        sbert_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        sbert_max_length: int = 512,
        whitening: bool = False,
        agg: nn.Module | None = None,
    ) -> None:
        if lambda_rank < 0:
            raise ValueError("lambda_rank must be >= 0.")
        if rank_temperature <= 0:
            raise ValueError("rank_temperature must be > 0.")
        super().__init__(
            data_dir=data_dir,
            instance_temperature=instance_temperature,
            graph_temperature=graph_temperature,
            dataset_name=dataset_name,
            sbert_model_name=sbert_model_name,
            sbert_max_length=sbert_max_length,
            whitening=whitening,
            agg=agg,
        )
        self.rank_temperature = rank_temperature
        self.lambda_rank = lambda_rank

    def forward(self, z: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """Combine MXCLR with the auxiliary teacher-order ListMLE ranking term."""
        if z.ndim != 2:
            raise ValueError(f"z must be [N, D], got {tuple(z.shape)}")
        batch_size = z.size(0)
        if batch_size < 2:
            raise RuntimeError("X-CLR requires batch_size >= 2.")
        if target.ndim != 2 or target.size(0) != batch_size:
            raise ValueError(
                f"target must be [N, L] or [N, N] with N={batch_size}, got {tuple(target.shape)}"
            )
        normalized_z = functional.normalize(z, dim=1)

        if target.shape == (batch_size, batch_size):
            g_soft = target
        else:
            g_soft = self.score_graph(target)
        return _compute_mxclr_rank_loss(
            z=normalized_z,
            g_soft=g_soft,
            instance_temperature=self.instance_temperature,
            graph_temperature=self.graph_temperature,
            rank_temperature=self.rank_temperature,
            lambda_rank=self.lambda_rank,
        )
