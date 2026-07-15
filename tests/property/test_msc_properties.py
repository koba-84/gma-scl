from __future__ import annotations

import pytest
import torch
from hypothesis import assume, given
from hypothesis import strategies as st

from src.models.loss.msc import _log_softmax_with_temperature


@st.composite
def matrix_and_mask(draw: st.DrawFn) -> tuple[torch.Tensor, torch.Tensor]:
    rows = draw(st.integers(min_value=1, max_value=6))
    cols = draw(st.integers(min_value=1, max_value=6))
    values = draw(
        st.lists(
            st.lists(
                st.floats(min_value=-20, max_value=20, allow_nan=False, allow_infinity=False),
                min_size=cols,
                max_size=cols,
            ),
            min_size=rows,
            max_size=rows,
        )
    )
    mask_values = draw(
        st.lists(
            st.lists(st.integers(min_value=0, max_value=1), min_size=cols, max_size=cols),
            min_size=rows,
            max_size=rows,
        )
    )
    assume(all(any(v == 1 for v in row) for row in mask_values))
    matrix = torch.tensor(values, dtype=torch.float32)
    mask = torch.tensor(mask_values, dtype=torch.float32)
    return matrix, mask


@given(
    matrix=st.lists(
        st.lists(
            st.floats(min_value=-10, max_value=10, allow_nan=False, allow_infinity=False),
            min_size=1,
            max_size=6,
        ),
        min_size=1,
        max_size=6,
    ),
    non_positive_temp=st.floats(max_value=0.0, allow_nan=False, allow_infinity=False),
)
def test_log_softmax_temp_rejects_non_positive_temperature(
    matrix: list[list[float]],
    non_positive_temp: float,
) -> None:
    cols = len(matrix[0])
    assume(all(len(row) == cols for row in matrix))
    tensor = torch.tensor(matrix, dtype=torch.float32)
    mask = torch.ones_like(tensor)
    with pytest.raises(ValueError, match="temperature must be > 0"):
        _log_softmax_with_temperature(
            matrix=tensor,
            temperature=non_positive_temp,
            mask=mask,
        )


@given(matrix_and_mask(), st.floats(min_value=0.05, max_value=5.0, allow_nan=False))
def test_log_softmax_temp_is_finite_on_active_mask_columns(
    inputs: tuple[torch.Tensor, torch.Tensor],
    temperature: float,
) -> None:
    matrix, mask = inputs
    output = _log_softmax_with_temperature(
        matrix=matrix,
        temperature=temperature,
        mask=mask,
    )
    active_values = output[mask > 0]
    assert active_values.numel() > 0
    assert torch.isfinite(active_values).all()
