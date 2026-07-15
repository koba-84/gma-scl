from __future__ import annotations

import torch


def blend_cosine_with_association(
    *,
    cosine: torch.Tensor,
    npmi: torch.Tensor,
    transport_lambda: float,
) -> torch.Tensor:
    """Return the cosine/NPMI association blend."""
    statistic = npmi.to(device=cosine.device, dtype=cosine.dtype)
    return ((1.0 - transport_lambda) * cosine) + (transport_lambda * statistic)
