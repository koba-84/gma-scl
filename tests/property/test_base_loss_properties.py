from __future__ import annotations

import pytest
import torch
from hypothesis import given
from hypothesis import strategies as st

from src.models.loss.base import Base


@given(
    batch_size=st.integers(min_value=2, max_value=8),
    feature_dim=st.integers(min_value=1, max_value=6),
    label_dim=st.integers(min_value=1, max_value=6),
)
def test_base_forward_rejects_labels_with_mismatched_shape(
    batch_size: int,
    feature_dim: int,
    label_dim: int,
) -> None:
    z = torch.randn(batch_size, feature_dim)
    invalid_labels = torch.zeros(batch_size + 1, label_dim)
    with pytest.raises(ValueError, match="labels must have shape"):
        Base().forward(z, invalid_labels)


@given(
    feature_dim=st.integers(min_value=1, max_value=8),
    label_dim=st.integers(min_value=1, max_value=8),
)
def test_base_forward_rejects_batch_size_below_two(
    feature_dim: int,
    label_dim: int,
) -> None:
    z = torch.randn(1, feature_dim)
    labels = torch.zeros(1, label_dim)
    with pytest.raises(RuntimeError, match="batch_size >= 2"):
        Base().forward(z, labels)
