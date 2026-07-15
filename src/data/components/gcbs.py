from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence, Sized

import numpy as np
import torch
import torch.nn.functional as F
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import reverse_cuthill_mckee
from torch.utils.data import Sampler


def compute_gcbs_permutation(
    embeddings: torch.Tensor,
    quantile: float,
    chunk_size: int,
) -> list[int]:
    """Compute GCBS permutation using reverse Cuthill-McKee on a sparsified graph."""
    if embeddings.ndim != 2:
        raise ValueError("embeddings must be a 2D tensor [num_samples, dim].")
    if not (0.0 < quantile < 1.0):
        raise ValueError("quantile must be in (0.0, 1.0).")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be >= 1.")

    num_samples = int(embeddings.shape[0])
    if num_samples == 0:
        return []
    if num_samples == 1:
        return [0]

    emb = embeddings.detach()
    if emb.device.type != "cpu":
        emb = emb.cpu()
    emb = F.normalize(emb.float(), dim=1)

    row_idx: list[torch.Tensor] = []
    col_idx: list[torch.Tensor] = []

    for start in range(0, num_samples, chunk_size):
        end = min(num_samples, start + chunk_size)
        chunk = emb[start:end]
        sim = torch.matmul(chunk, emb.T)

        for i in range(start, end):
            sim[i - start, i] = -float("inf")

        thresholds = torch.quantile(sim, quantile, dim=1, keepdim=True)
        mask = sim >= thresholds
        rows, cols = mask.nonzero(as_tuple=True)
        if rows.numel() == 0:
            continue
        row_idx.append(rows + start)
        col_idx.append(cols)

    if not row_idx:
        return list(range(num_samples))

    row_idx_np = torch.cat(row_idx).cpu().numpy()
    col_idx_np = torch.cat(col_idx).cpu().numpy()
    data = np.ones_like(row_idx_np, dtype=np.uint8)

    graph = csr_matrix((data, (row_idx_np, col_idx_np)), shape=(num_samples, num_samples))
    graph = graph.maximum(graph.transpose())
    perm = reverse_cuthill_mckee(graph, symmetric_mode=True)
    return perm.tolist()


class GCBSSampler(Sampler[int]):
    """Sampler that iterates over a mutable permutation."""

    def __init__(self, data_source: Sized, indices: Sequence[int] | None = None) -> None:
        self.data_source = data_source
        if indices is None:
            self._indices = list(range(len(data_source)))
        else:
            self._indices = list(indices)

    def set_indices(self, indices: Iterable[int]) -> None:
        """Set the explicit sampling order indices."""
        self._indices = list(indices)

    def __iter__(self) -> Iterator[int]:
        return iter(self._indices)

    def __len__(self) -> int:
        return len(self.data_source)


if __name__ == "__main__":
    embeddings = torch.tensor(
        [
            [1.0, 0.0, 0.0],
            [0.9, 0.1, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.9, 0.1],
            [0.0, 0.0, 1.0],
        ],
        dtype=torch.float32,
    )
    perm = compute_gcbs_permutation(embeddings=embeddings, quantile=0.8, chunk_size=2)
    assert sorted(perm) == list(range(embeddings.shape[0]))
    assert len(perm) == embeddings.shape[0]

    assert compute_gcbs_permutation(torch.empty((0, 4), dtype=torch.float32), 0.5, 1) == []
    assert compute_gcbs_permutation(torch.tensor([[1.0, 0.0]], dtype=torch.float32), 0.5, 1) == [0]

    invalid_cases = [
        (torch.ones(2, 2, 2), 0.5, 1),
        (torch.ones(2, 2), 0.0, 1),
        (torch.ones(2, 2), 1.0, 1),
        (torch.ones(2, 2), 0.5, 0),
    ]
    for emb, q, chunk in invalid_cases:
        try:
            _ = compute_gcbs_permutation(embeddings=emb, quantile=q, chunk_size=chunk)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid GCBS inputs must raise ValueError")

    sampler = GCBSSampler(data_source=list(range(5)))
    assert list(iter(sampler)) == [0, 1, 2, 3, 4]
    assert len(sampler) == 5
    sampler.set_indices([4, 2, 0])
    assert list(iter(sampler)) == [4, 2, 0]
    assert len(sampler) == 5

    print("GCBS self-test passed.")
