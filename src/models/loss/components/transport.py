"""MXCLR transport helpers."""

from __future__ import annotations

from typing import Literal

import ot
import torch

type TransportStrategy = Literal["wmd", "wrd", "uot"]


def _canonicalize_label_sets(
    labels_bin: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    active_label_masks = labels_bin > 0
    unique_label_masks, inverse = torch.unique(active_label_masks, dim=0, return_inverse=True)
    unique_sizes = unique_label_masks.sum(dim=1).to(dtype=torch.long)
    max_size = int(unique_sizes.max().item()) if unique_sizes.numel() > 0 else 0
    unique_indices = torch.full(
        (unique_label_masks.size(0), max_size),
        -1,
        device=labels_bin.device,
        dtype=torch.long,
    )

    with torch.no_grad():
        for row_idx in range(unique_label_masks.size(0)):
            active_indices = torch.nonzero(unique_label_masks[row_idx], as_tuple=False).flatten()
            if active_indices.numel() > 0:
                unique_indices[row_idx, : active_indices.numel()] = active_indices

    return unique_sizes, unique_indices, inverse


def _validate_pairwise_inputs(
    labels_bin: torch.Tensor,
    cost_matrix: torch.Tensor,
    label_weights: torch.Tensor,
) -> tuple[torch.device, torch.dtype]:
    if labels_bin.ndim != 2:
        raise ValueError(f"labels_bin must be [N, L], got {tuple(labels_bin.shape)}")
    if cost_matrix.ndim != 2 or cost_matrix.size(0) != cost_matrix.size(1):
        raise ValueError(f"cost_matrix must be a square matrix, got {tuple(cost_matrix.shape)}")
    if labels_bin.size(1) != cost_matrix.size(0):
        raise ValueError(
            "Label dimension mismatch: "
            f"labels have L={labels_bin.size(1)}, cost matrix is {tuple(cost_matrix.shape)}."
        )
    if label_weights.ndim != 1 or label_weights.size(0) != labels_bin.size(1):
        raise ValueError(
            "label_weights must be [L], got "
            f"{tuple(label_weights.shape)} for L={labels_bin.size(1)}."
        )
    return labels_bin.device, labels_bin.dtype


def pairwise_transport(
    labels_bin: torch.Tensor,
    cost_matrix: torch.Tensor,
    label_weights: torch.Tensor,
    *,
    strategy: TransportStrategy,
    sinkhorn_reg: float = 1e-1,
    sinkhorn_max_iter: int = 100,
    sinkhorn_tol: float = 1e-3,
    uot_reg_m: float = 1.0,
) -> torch.Tensor:
    """Return the pairwise transport distance matrix for the selected strategy."""
    if strategy not in {"wmd", "wrd", "uot"}:
        raise ValueError(f"strategy must be one of ('wmd', 'wrd', 'uot'), got {strategy!r}.")
    if sinkhorn_reg <= 0.0:
        raise ValueError(f"sinkhorn reg must be > 0, got {sinkhorn_reg}.")
    if sinkhorn_max_iter <= 0:
        raise ValueError(f"sinkhorn max_iter must be > 0, got {sinkhorn_max_iter}.")
    if sinkhorn_tol <= 0.0:
        raise ValueError(f"sinkhorn tol must be > 0, got {sinkhorn_tol}.")
    if strategy == "uot" and uot_reg_m <= 0.0:
        raise ValueError(f"uot reg_m must be > 0, got {uot_reg_m}.")

    device, output_dtype = _validate_pairwise_inputs(labels_bin, cost_matrix, label_weights)
    if labels_bin.size(0) == 0:
        return torch.empty((0, 0), device=device, dtype=output_dtype)

    solver_cost = cost_matrix.detach().to(device=device, dtype=torch.float64)
    solver_weights = label_weights.detach().to(device=device, dtype=torch.float64)
    backend = ot.backend.get_backend(solver_cost, solver_weights)
    if not isinstance(backend, ot.backend.TorchBackend):
        raise RuntimeError("MXCLR transport requires POT torch backend.")

    unique_sizes, unique_indices, inverse = _canonicalize_label_sets(labels_bin)
    unique_count = unique_sizes.size(0)
    unique_distance = torch.empty((unique_count, unique_count), device=device, dtype=output_dtype)

    with torch.no_grad():
        for i in range(unique_count):
            size_i = int(unique_sizes[i].item())
            for j in range(i, unique_count):
                size_j = int(unique_sizes[j].item())

                if size_i == 0 and size_j == 0:
                    distance = unique_distance.new_tensor(0.0)
                elif size_i == 0 or size_j == 0:
                    distance = unique_distance.new_tensor(2.0)
                elif i == j:
                    distance = unique_distance.new_tensor(0.0)
                else:
                    source_idx = unique_indices[i, :size_i]
                    target_idx = unique_indices[j, :size_j]
                    source_mass = solver_weights.index_select(0, source_idx)
                    target_mass = solver_weights.index_select(0, target_idx)
                    pair_cost = solver_cost.index_select(0, source_idx).index_select(1, target_idx)

                    if torch.any(source_mass <= 0.0) or torch.any(target_mass <= 0.0):
                        raise ValueError("Active-label mass must be > 0.")

                    if strategy == "uot":
                        distance = ot.unbalanced.sinkhorn_unbalanced2(
                            source_mass,
                            target_mass,
                            pair_cost,
                            reg=sinkhorn_reg,
                            reg_m=uot_reg_m,
                            method="sinkhorn",
                            returnCost="linear",
                            numItermax=sinkhorn_max_iter,
                            stopThr=sinkhorn_tol,
                            warn=False,
                        )
                    else:
                        source_mass = source_mass / backend.sum(source_mass)
                        target_mass = target_mass / backend.sum(target_mass)
                        distance = ot.sinkhorn2(
                            source_mass,
                            target_mass,
                            pair_cost,
                            reg=sinkhorn_reg,
                            method="sinkhorn",
                            numItermax=sinkhorn_max_iter,
                            stopThr=sinkhorn_tol,
                            warn=False,
                        )

                    distance = torch.as_tensor(distance, device=device, dtype=output_dtype)

                unique_distance[i, j] = distance
                unique_distance[j, i] = distance

    return unique_distance.index_select(0, inverse).index_select(1, inverse)
