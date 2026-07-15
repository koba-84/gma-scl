from __future__ import annotations

import hydra
import pytest
import torch

from src.models.loss.msc import MSC


def test_msc_requires_prototype() -> None:
    z = torch.tensor(
        [
            [0.5, 1.0, 0.0],
            [0.6, 0.8, 0.1],
            [0.0, -0.7, 0.9],
            [0.2, -0.4, 1.1],
        ],
        dtype=torch.float32,
    )
    labels = torch.tensor(
        [
            [1, 1, 0],
            [1, 0, 0],
            [0, 1, 1],
            [0, 0, 1],
        ],
        dtype=torch.float32,
    )

    with pytest.raises(ValueError, match="prototype is required"):
        MSC(alpha=1.0, beta=1.0, temperature=0.07)(z, labels)


def test_msc_forward_returns_finite_scalar() -> None:
    z = torch.tensor(
        [
            [0.5, 1.0, 0.0],
            [0.6, 0.8, 0.1],
            [0.0, -0.7, 0.9],
            [0.2, -0.4, 1.1],
        ],
        dtype=torch.float32,
    )
    labels = torch.tensor(
        [
            [1, 1, 0],
            [1, 0, 0],
            [0, 1, 1],
            [0, 0, 1],
        ],
        dtype=torch.float32,
    )
    prototype = torch.tensor(
        [
            [0.55, 0.9, 0.05],
            [0.2, 0.15, 0.45],
            [0.1, -0.55, 1.0],
        ],
        dtype=torch.float32,
    )

    out = MSC(alpha=1.0, beta=1.0, temperature=0.07)(z, labels, prototype=prototype)

    assert out.ndim == 0
    assert torch.isfinite(out)


def test_msc_forward_is_invariant_to_rowwise_feature_scaling() -> None:
    z = torch.tensor(
        [
            [0.5, 1.0, 0.0],
            [0.6, 0.8, 0.1],
            [0.0, -0.7, 0.9],
            [0.2, -0.4, 1.1],
        ],
        dtype=torch.float32,
    )
    scales = torch.tensor([[2.0], [0.5], [3.0], [1.5]], dtype=torch.float32)
    labels = torch.tensor(
        [
            [1, 1, 0],
            [1, 0, 0],
            [0, 1, 1],
            [0, 0, 1],
        ],
        dtype=torch.float32,
    )
    prototype = torch.tensor(
        [
            [0.55, 0.9, 0.05],
            [0.2, 0.15, 0.45],
            [0.1, -0.55, 1.0],
        ],
        dtype=torch.float32,
    )
    loss_fn = MSC(alpha=1.0, beta=1.0, temperature=0.07)

    assert torch.allclose(loss_fn(z, labels, prototype), loss_fn(z * scales, labels, prototype))


def test_hydra_instantiates_msc(compose_train_config) -> None:
    msc_cfg = compose_train_config(["contrastive/model=msc"])
    msc_instance = hydra.utils.instantiate(msc_cfg.contrastive.model.loss_fn)

    assert isinstance(msc_instance, MSC)
