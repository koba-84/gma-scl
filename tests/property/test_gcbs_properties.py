from __future__ import annotations

import torch
from hypothesis import assume, given
from hypothesis import strategies as st

from src.data.components.gcbs import compute_gcbs_permutation


@st.composite
def gcbs_inputs(draw: st.DrawFn) -> tuple[torch.Tensor, float, int]:
    """Generate valid inputs for GCBS permutation property tests."""
    num_samples = draw(st.integers(min_value=0, max_value=8))
    dim = draw(st.integers(min_value=1, max_value=6))
    quantile = draw(st.floats(min_value=0.05, max_value=0.95, allow_nan=False))
    chunk_size = draw(st.integers(min_value=1, max_value=5))

    if num_samples == 0:
        return torch.empty((0, dim), dtype=torch.float32), quantile, chunk_size

    rows = draw(
        st.lists(
            st.lists(
                st.floats(min_value=-10, max_value=10, allow_nan=False, allow_infinity=False),
                min_size=dim,
                max_size=dim,
            ),
            min_size=num_samples,
            max_size=num_samples,
        )
    )
    assume(all(any(abs(v) > 1e-6 for v in row) for row in rows))
    embeddings = torch.tensor(rows, dtype=torch.float32)
    return embeddings, quantile, chunk_size


@given(gcbs_inputs())
def test_compute_gcbs_permutation_returns_valid_permutation(
    args: tuple[torch.Tensor, float, int],
) -> None:
    embeddings, quantile, chunk_size = args
    permutation = compute_gcbs_permutation(
        embeddings=embeddings,
        quantile=quantile,
        chunk_size=chunk_size,
    )

    assert len(permutation) == int(embeddings.shape[0])
    assert sorted(permutation) == list(range(int(embeddings.shape[0])))


@given(
    quantile=st.one_of(
        st.floats(max_value=0.0, allow_nan=False, allow_infinity=False),
        st.floats(min_value=1.0, allow_nan=False, allow_infinity=False),
    )
)
def test_compute_gcbs_permutation_rejects_invalid_quantile(quantile: float) -> None:
    embeddings = torch.randn(3, 4)
    try:
        compute_gcbs_permutation(embeddings=embeddings, quantile=quantile, chunk_size=2)
    except ValueError:
        return
    raise AssertionError("expected ValueError for invalid quantile")


@given(chunk_size=st.integers(max_value=0))
def test_compute_gcbs_permutation_rejects_non_positive_chunk_size(chunk_size: int) -> None:
    embeddings = torch.randn(3, 4)
    try:
        compute_gcbs_permutation(embeddings=embeddings, quantile=0.5, chunk_size=chunk_size)
    except ValueError:
        return
    raise AssertionError("expected ValueError for non-positive chunk_size")


@given(
    as_list=st.lists(
        st.floats(min_value=-5, max_value=5, allow_nan=False, allow_infinity=False),
        min_size=1,
        max_size=8,
    )
)
def test_compute_gcbs_permutation_rejects_non_2d_embeddings(as_list: list[float]) -> None:
    embeddings = torch.tensor(as_list, dtype=torch.float32)
    try:
        compute_gcbs_permutation(embeddings=embeddings, quantile=0.5, chunk_size=2)
    except ValueError:
        return
    raise AssertionError("expected ValueError for non-2d embeddings")


@given(dim=st.integers(min_value=1, max_value=8))
def test_compute_gcbs_permutation_returns_empty_for_empty_input(dim: int) -> None:
    permutation = compute_gcbs_permutation(
        embeddings=torch.empty((0, dim), dtype=torch.float32),
        quantile=0.5,
        chunk_size=2,
    )
    assert permutation == []


@given(
    row=st.lists(
        st.floats(min_value=-10, max_value=10, allow_nan=False, allow_infinity=False),
        min_size=1,
        max_size=8,
    )
)
def test_compute_gcbs_permutation_returns_identity_for_single_input(row: list[float]) -> None:
    assume(any(abs(value) > 1e-6 for value in row))
    permutation = compute_gcbs_permutation(
        embeddings=torch.tensor([row], dtype=torch.float32),
        quantile=0.5,
        chunk_size=2,
    )
    assert permutation == [0]
