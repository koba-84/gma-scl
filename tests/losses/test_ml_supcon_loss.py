from __future__ import annotations

import pytest
import torch
import torch.nn.functional as functional

from src.models.loss.base import Base
from src.models.loss.ml_supcon import MulSupCon


def _manual_mulsupcon(
    z: torch.Tensor,
    labels: torch.Tensor,
    *,
    temperature: float,
) -> torch.Tensor:
    normalized_z = functional.normalize(z, dim=1)
    rows: list[torch.Tensor] = []

    for anchor_idx in range(labels.size(0)):
        for label_idx in range(labels.size(1)):
            if labels[anchor_idx, label_idx] <= 0:
                continue

            logits = []
            positive_columns = []
            kept_columns = []

            for ref_idx in range(labels.size(0)):
                if ref_idx == anchor_idx:
                    continue
                logits.append(
                    torch.dot(normalized_z[anchor_idx], normalized_z[ref_idx]) / temperature
                )
                kept_columns.append(ref_idx)
                if labels[ref_idx, label_idx] > 0:
                    positive_columns.append(len(kept_columns) - 1)

            if not logits or not positive_columns:
                rows.append(z.new_tensor(0.0))
                continue

            row_logits = torch.stack(logits)
            log_prob = row_logits - torch.logsumexp(row_logits, dim=0)
            rows.append(-log_prob[positive_columns].mean())

    if not rows:
        return z.new_tensor(0.0)
    return torch.stack(rows).mean()


def test_ml_supcon_forward_matches_labelwise_reference() -> None:
    z = torch.tensor(
        [
            [1.0, 0.0, 0.5],
            [0.9, 0.1, 0.4],
            [0.2, 1.1, 0.3],
            [0.0, 0.8, 0.6],
        ],
        dtype=torch.float32,
    )
    labels = torch.tensor(
        [
            [1, 1, 0],
            [1, 0, 0],
            [0, 1, 1],
            [0, 1, 0],
        ],
        dtype=torch.float32,
    )

    actual = MulSupCon(temperature=0.2)(z, labels)
    expected = _manual_mulsupcon(z, labels, temperature=0.2)

    assert actual.ndim == 0
    assert torch.isfinite(actual)
    assert torch.allclose(actual, expected, atol=1e-6)


def test_ml_supcon_forward_rejects_invalid_labels_shape() -> None:
    z = torch.randn(4, 3)
    labels = torch.tensor([1.0, 0.0, 1.0], dtype=torch.float32)

    with pytest.raises(ValueError, match="labels must have shape"):
        MulSupCon(temperature=0.07)(z, labels)


def test_ml_supcon_differs_from_base_objective() -> None:
    z = torch.tensor(
        [
            [1.0, 0.0, 0.3],
            [0.7, 0.2, 0.5],
            [0.1, 1.0, 0.4],
            [0.2, 0.6, 0.8],
        ],
        dtype=torch.float32,
    )
    labels = torch.tensor(
        [
            [1, 1, 0],
            [1, 0, 0],
            [0, 1, 1],
            [0, 1, 0],
        ],
        dtype=torch.float32,
    )

    mulsupcon = MulSupCon(temperature=0.2)(z, labels)
    base = Base(temperature=0.2)(z, labels)

    assert not torch.isclose(mulsupcon, base)


def test_ml_supcon_forward_is_invariant_to_rowwise_feature_scaling() -> None:
    z = torch.tensor(
        [
            [1.0, 0.0, 0.3],
            [0.7, 0.2, 0.5],
            [0.1, 1.0, 0.4],
            [0.2, 0.6, 0.8],
        ],
        dtype=torch.float32,
    )
    scales = torch.tensor([[2.0], [0.5], [3.0], [1.5]], dtype=torch.float32)
    labels = torch.tensor(
        [
            [1, 1, 0],
            [1, 0, 0],
            [0, 1, 1],
            [0, 1, 0],
        ],
        dtype=torch.float32,
    )
    loss_fn = MulSupCon(temperature=0.2)

    assert torch.allclose(loss_fn(z, labels), loss_fn(z * scales, labels), atol=1e-6)
