from __future__ import annotations

import math
from collections.abc import Iterator, Sized

import numpy as np
import torch
from dppy.finite_dpps import FiniteDPP
from torch.utils.data import BatchSampler


class DPPBatchSampler(BatchSampler):
    """Batch sampler that draws k-DPP batches without replacement within an epoch."""

    def __init__(
        self,
        data_source: Sized,
        batch_size: int,
        drop_last: bool = False,
        mode: str = "GS_bis",
        random_state: int | None = None,
    ) -> None:
        self.data_source = data_source
        self.batch_size = int(batch_size)
        self.drop_last = bool(drop_last)
        self.mode = mode
        self._seed = random_state
        self._rng = np.random.RandomState(random_state) if random_state is not None else None
        self._phi: np.ndarray | None = None
        self._remaining: list[int] = []

    def set_embeddings(self, embeddings: torch.Tensor | np.ndarray) -> None:
        """Set embeddings used by the sampler for selection."""
        if isinstance(embeddings, torch.Tensor):
            emb = embeddings.detach().cpu().double().numpy()
        else:
            emb = np.asarray(embeddings, dtype=np.float64)

        if emb.ndim != 2:
            raise ValueError("embeddings must be a 2D array [num_samples, dim].")
        if emb.shape[0] != len(self.data_source):
            raise ValueError("embeddings size does not match dataset length.")

        # DPPy expects L_gram_factor = Phi with shape (d, N)
        self._phi = emb.T
        self._remaining = list(range(emb.shape[0]))
        if self._seed is not None:
            self._rng = np.random.RandomState(self._seed)

    def is_initialized(self) -> bool:
        """Return whether required sampler state has been initialized."""
        return self._phi is not None

    def __iter__(self) -> Iterator[list[int]]:
        if self._phi is None:
            raise RuntimeError("DPPBatchSampler is not initialized. Call set_embeddings() first.")

        remaining = list(self._remaining)
        d = int(self._phi.shape[0])

        while remaining:
            k = min(self.batch_size, len(remaining))
            if self.drop_last and k < self.batch_size:
                break
            if k > d:
                raise ValueError(
                    f"k-DPP batch size {k} exceeds embedding dimension {d}. "
                    "Reduce batch_size or increase embedding dimension."
                )

            phi_subset = self._phi[:, remaining]
            dpp = FiniteDPP(kernel_type="likelihood", L_gram_factor=phi_subset)
            sample = dpp.sample_exact_k_dpp(size=k, mode=self.mode, random_state=self._rng)

            chosen_pos = set(sample)
            batch_indices = [remaining[i] for i in sample]
            remaining = [idx for i, idx in enumerate(remaining) if i not in chosen_pos]

            yield batch_indices

    def __len__(self) -> int:
        n = len(self.data_source)
        if self.drop_last:
            return n // self.batch_size
        return math.ceil(n / self.batch_size)


if __name__ == "__main__":
    not_initialized = DPPBatchSampler(data_source=list(range(4)), batch_size=2)
    try:
        _ = list(iter(not_initialized))
    except RuntimeError:
        pass
    else:
        raise AssertionError("Iteration before set_embeddings must raise RuntimeError")

    invalid_shape = DPPBatchSampler(data_source=list(range(4)), batch_size=2)
    try:
        invalid_shape.set_embeddings(np.ones((4,), dtype=np.float64))
    except ValueError:
        pass
    else:
        raise AssertionError("1D embeddings must raise ValueError")
    try:
        invalid_shape.set_embeddings(np.ones((3, 4), dtype=np.float64))
    except ValueError:
        pass
    else:
        raise AssertionError("Mismatched embedding rows must raise ValueError")

    sampler = DPPBatchSampler(data_source=list(range(4)), batch_size=2, random_state=0)
    sampler.set_embeddings(torch.eye(4, dtype=torch.float32))
    batches = list(iter(sampler))
    flat = [idx for batch in batches for idx in batch]
    assert sorted(flat) == [0, 1, 2, 3]
    assert len(flat) == len(set(flat))
    assert all(len(batch) <= 2 for batch in batches)

    drop_last = DPPBatchSampler(data_source=list(range(5)), batch_size=2, drop_last=True, random_state=0)
    drop_last.set_embeddings(torch.eye(5, dtype=torch.float32))
    drop_last_batches = list(iter(drop_last))
    assert len(drop_last) == 2
    assert len(drop_last_batches) == 2
    assert sum(len(batch) for batch in drop_last_batches) == 4

    too_large = DPPBatchSampler(data_source=list(range(4)), batch_size=3)
    too_large.set_embeddings(torch.randn(4, 2, dtype=torch.float32))
    try:
        for _batch in too_large:
            break
    except ValueError:
        pass
    else:
        raise AssertionError("k > embedding dimension must raise ValueError")

    print("DPPBatchSampler self-test passed.")
