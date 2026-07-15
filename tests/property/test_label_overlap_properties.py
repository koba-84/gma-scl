from __future__ import annotations

import torch
from hypothesis import given
from hypothesis import strategies as st

from src.models.loss.components.label_overlap import compute_or_counts


@st.composite
def binary_label_pair(draw: st.DrawFn) -> tuple[torch.Tensor, torch.Tensor]:
    labels = draw(st.integers(min_value=1, max_value=8))
    rows_a = draw(st.integers(min_value=1, max_value=8))
    rows_b = draw(st.integers(min_value=1, max_value=8))

    values_a = draw(
        st.lists(
            st.lists(st.integers(min_value=0, max_value=1), min_size=labels, max_size=labels),
            min_size=rows_a,
            max_size=rows_a,
        )
    )
    values_b = draw(
        st.lists(
            st.lists(st.integers(min_value=0, max_value=1), min_size=labels, max_size=labels),
            min_size=rows_b,
            max_size=rows_b,
        )
    )
    tensor_a = torch.tensor(values_a, dtype=torch.float32)
    tensor_b = torch.tensor(values_b, dtype=torch.float32)
    return tensor_a, tensor_b


@given(binary_label_pair())
def test_compute_or_is_commutative_and_bounded(
    inputs: tuple[torch.Tensor, torch.Tensor],
) -> None:
    query, key = inputs
    result = compute_or_counts(query, key)
    swapped = compute_or_counts(key, query).T

    assert torch.equal(result, swapped)
    assert torch.all(result >= 0)
    assert torch.all(result <= query.shape[1])
