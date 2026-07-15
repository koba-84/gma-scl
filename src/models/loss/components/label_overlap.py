from __future__ import annotations

import torch


def compute_or_counts(query_tensor: torch.Tensor, key_tensor: torch.Tensor) -> torch.Tensor:
    """Return pairwise label-wise OR counts for binary multi-label matrices."""
    or_build = query_tensor.unsqueeze(1) + key_tensor.unsqueeze(0)
    or_build = (or_build > 0).to(query_tensor.dtype)
    return or_build.sum(dim=2)
