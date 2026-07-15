from __future__ import annotations

import pytest
import torch

from src.models.loss.base import Base


def test_base_forward_returns_finite_scalar() -> None:
    z = torch.tensor(
        [
            [1.0, 0.0, 0.5],
            [0.8, 0.2, 0.4],
            [-0.3, 0.9, 0.1],
            [0.0, -0.4, 1.2],
        ],
        dtype=torch.float32,
    )
    labels = torch.tensor(
        [
            [1, 0, 1],
            [1, 0, 0],
            [0, 1, 0],
            [0, 1, 1],
        ],
        dtype=torch.float32,
    )

    out = Base(temperature=0.07)(z, labels)

    assert out.ndim == 0
    assert torch.isfinite(out)


def test_base_forward_without_positive_pairs_keeps_grad_graph() -> None:
    z = torch.tensor(
        [
            [1.0, 0.2, -0.5],
            [0.3, -0.7, 1.1],
            [-0.8, 0.4, 0.6],
        ],
        dtype=torch.float32,
        requires_grad=True,
    )
    labels = torch.tensor(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ],
        dtype=torch.float32,
    )

    out = Base(temperature=0.07)(z, labels)

    assert float(out.detach()) == pytest.approx(0.0)
    assert out.requires_grad
    assert out.grad_fn is not None

    out.backward()
    assert z.grad is not None
    assert torch.allclose(z.grad, torch.zeros_like(z))


def test_base_forward_is_invariant_to_rowwise_feature_scaling() -> None:
    z = torch.tensor(
        [
            [1.0, 0.0, 0.5],
            [0.8, 0.2, 0.4],
            [-0.3, 0.9, 0.1],
            [0.0, -0.4, 1.2],
        ],
        dtype=torch.float32,
    )
    scales = torch.tensor([[2.0], [0.5], [3.0], [1.5]], dtype=torch.float32)
    labels = torch.tensor(
        [
            [1, 0, 1],
            [1, 0, 0],
            [0, 1, 0],
            [0, 1, 1],
        ],
        dtype=torch.float32,
    )

    loss_fn = Base(temperature=0.07)
    out = loss_fn(z, labels)
    out_scaled = loss_fn(z * scales, labels)

    assert torch.allclose(out, out_scaled, atol=1e-6)
