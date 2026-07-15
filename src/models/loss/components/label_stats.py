from __future__ import annotations

import csv
import sys
import tempfile
import uuid
from pathlib import Path

csv.field_size_limit(sys.maxsize)

import numpy as np
import torch


def _load_counts_from_train_csv(
    csv_path: Path,
    positive_threshold: float,
) -> tuple[np.ndarray, np.ndarray, int]:
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None or len(header) < 2:
            raise ValueError("CSV must have at least two columns: text + labels.")

        n_labels = len(header) - 1
        label_counts = np.zeros(n_labels, dtype=np.int64)
        pair_counts = np.zeros((n_labels, n_labels), dtype=np.int64)

        n_docs = 0
        for line_no, row in enumerate(reader, start=2):
            if len(row) < len(header):
                raise ValueError(
                    f"Row has fewer columns than header at line {line_no}: "
                    f"{len(row)} < {len(header)}"
                )
            n_docs += 1

            positive_indices: list[int] = []
            for idx, raw in enumerate(row[1:], start=0):
                try:
                    value = float(raw)
                except ValueError as exc:
                    raise ValueError(
                        f"Invalid label value at line {line_no}, column {idx + 2}: {raw!r}"
                    ) from exc
                if value > positive_threshold:
                    positive_indices.append(idx)

            if not positive_indices:
                continue

            label_counts[positive_indices] += 1
            for i_pos, i in enumerate(positive_indices):
                pair_counts[i, i] += 1
                for j in positive_indices[i_pos + 1 :]:
                    pair_counts[i, j] += 1
                    pair_counts[j, i] += 1

    if n_docs == 0:
        raise ValueError(f"No data rows found in CSV: {csv_path}")
    return label_counts, pair_counts, n_docs


def compute_idf(
    data_dir: str | Path,
    dataset_name: str,
    positive_threshold: float = 0.0,
) -> torch.Tensor:
    """Compute train.csv-derived label IDF values as float32."""
    path = Path(data_dir) / dataset_name / "train.csv"
    if not path.exists():
        raise FileNotFoundError(f"Training CSV for label statistics not found: {path}")
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Training label source must be .csv format: {path}")

    label_counts, _, n_docs = _load_counts_from_train_csv(
        csv_path=path,
        positive_threshold=positive_threshold,
    )
    idf = np.log((1.0 + float(n_docs)) / (1.0 + label_counts.astype(np.float64))) + 1.0
    return torch.from_numpy(idf).to(dtype=torch.float32)


def compute_frequency(
    data_dir: str | Path,
    dataset_name: str,
    positive_threshold: float = 0.0,
) -> torch.Tensor:
    """Compute train.csv-derived label frequency counts as float32."""
    path = Path(data_dir) / dataset_name / "train.csv"
    if not path.exists():
        raise FileNotFoundError(f"Training CSV for label statistics not found: {path}")
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Training label source must be .csv format: {path}")

    label_counts, _, _ = _load_counts_from_train_csv(
        csv_path=path,
        positive_threshold=positive_threshold,
    )
    return torch.from_numpy(label_counts.astype(np.float32))


def compute_npmi(
    data_dir: str | Path,
    dataset_name: str,
    positive_threshold: float = 0.0,
) -> torch.Tensor:
    """Compute train.csv-derived pairwise NPMI and map it from [-1, 1] to [0, 1]."""
    path = Path(data_dir) / dataset_name / "train.csv"
    if not path.exists():
        raise FileNotFoundError(f"Training CSV for label statistics not found: {path}")
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Training label source must be .csv format: {path}")

    label_counts, pair_counts, n_docs = _load_counts_from_train_csv(
        csv_path=path,
        positive_threshold=positive_threshold,
    )
    pi = label_counts.astype(np.float64) / float(n_docs)
    pij = pair_counts.astype(np.float64) / float(n_docs)
    pi_outer = np.outer(pi, pi)

    npmi = np.zeros_like(pij, dtype=np.float64)
    valid = (pij > 0.0) & (pi_outer > 0.0)
    if np.any(valid):
        with np.errstate(divide="ignore", invalid="ignore"):
            pmi = np.log(pij[valid] / pi_outer[valid])
            denom = -np.log(pij[valid])
            npmi[valid] = pmi / denom

    npmi = np.clip(npmi, -1.0, 1.0)
    np.fill_diagonal(npmi, 1.0)
    return ((torch.from_numpy(npmi).to(dtype=torch.float32) + 1.0) * 0.5).clamp(0.0, 1.0)


def compute_yules_q(
    data_dir: str | Path,
    dataset_name: str,
    positive_threshold: float = 0.0,
) -> torch.Tensor:
    """Compute Haldane-Anscombe-corrected pairwise Yule's Q mapped to [0, 1]."""
    path = Path(data_dir) / dataset_name / "train.csv"
    if not path.exists():
        raise FileNotFoundError(f"Training CSV for label statistics not found: {path}")
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Training label source must be .csv format: {path}")

    label_counts, pair_counts, n_docs = _load_counts_from_train_csv(
        csv_path=path,
        positive_threshold=positive_threshold,
    )
    pair_counts_float = pair_counts.astype(np.float64)
    label_counts_float = label_counts.astype(np.float64)

    a = pair_counts_float + 0.5
    b = label_counts_float[:, None] - pair_counts_float + 0.5
    c = label_counts_float[None, :] - pair_counts_float + 0.5
    d = (
        float(n_docs)
        - label_counts_float[:, None]
        - label_counts_float[None, :]
        + pair_counts_float
        + 0.5
    )

    numerator = (a * d) - (b * c)
    denominator = (a * d) + (b * c)
    yules_q = np.divide(
        numerator,
        denominator,
        out=np.zeros_like(numerator, dtype=np.float64),
        where=denominator != 0.0,
    )

    yules_q = np.clip(yules_q, -1.0, 1.0)
    np.fill_diagonal(yules_q, 1.0)
    return ((torch.from_numpy(yules_q).to(dtype=torch.float32) + 1.0) * 0.5).clamp(0.0, 1.0)


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[4]
    tmp_dir = repo_root / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    test_dir = Path(
        tempfile.mkdtemp(prefix=f"label_stats_selftest_{uuid.uuid4().hex}_", dir=tmp_dir)
    )
    dataset_name = "label_stats_selftest_dataset"
    dataset_dir = test_dir / dataset_name
    dataset_dir.mkdir(parents=True, exist_ok=True)
    train_csv_path = dataset_dir / "train.csv"

    try:
        train_csv_path.write_text(
            "\n".join(
                [
                    "text,label_a,label_b,label_c",
                    "doc1,1,0,1",
                    "doc2,1,0,0",
                    "doc3,0,1,0",
                    "doc4,0,1,1",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        frequency = compute_frequency(test_dir, dataset_name)
        idf = compute_idf(test_dir, dataset_name)
        npmi = compute_npmi(test_dir, dataset_name)
        yules_q = compute_yules_q(test_dir, dataset_name)
        assert frequency.shape == (3,)
        assert idf.shape == (3,)
        assert npmi.shape == (3, 3)
        assert yules_q.shape == (3, 3)
        assert torch.equal(frequency, torch.tensor([2.0, 2.0, 2.0], dtype=torch.float32))
        assert torch.isfinite(idf).all()
        assert torch.isfinite(npmi).all()
        assert torch.isfinite(yules_q).all()
        assert torch.allclose(npmi.diag(), torch.ones(3, dtype=torch.float32))
        assert torch.allclose(yules_q.diag(), torch.ones(3, dtype=torch.float32))
        print("label_stats self-test passed.")
    finally:
        if train_csv_path.exists():
            train_csv_path.unlink()
        if dataset_dir.exists():
            dataset_dir.rmdir()
        if test_dir.exists():
            test_dir.rmdir()
