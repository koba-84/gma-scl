#!/usr/bin/env python3
"""Build an NPMI matrix from multi-label CSV data.

Expected CSV format:
- first column: text
- remaining columns: label indicators (0/1 or float)
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build NPMI matrix from train.csv")
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to input CSV (e.g., data/aapd/train.csv)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Path to output .npy. If omitted, '<input_dir>/npmi.npy' is used.",
    )
    parser.add_argument(
        "--positive-threshold",
        type=float,
        default=0.0,
        help="Values greater than this threshold are treated as positive labels.",
    )
    return parser.parse_args()


def _load_counts(
    csv_path: Path, positive_threshold: float
) -> tuple[np.ndarray, np.ndarray, list[str], int]:
    if not csv_path.exists():
        raise FileNotFoundError(f"Input CSV not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None or len(header) < 2:
            raise ValueError("CSV must have at least two columns: text + labels.")

        label_columns = [h.strip() for h in header[1:]]
        n_labels = len(label_columns)
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

    return label_counts, pair_counts, label_columns, n_docs


def _compute_npmi(label_counts: np.ndarray, pair_counts: np.ndarray, n_docs: int) -> np.ndarray:
    pi = label_counts.astype(np.float64) / float(n_docs)
    pij = pair_counts.astype(np.float64) / float(n_docs)
    pi_outer = np.outer(pi, pi)

    npmi = np.zeros_like(pij, dtype=np.float64)
    valid = (pij > 0.0) & (pi_outer > 0.0)
    if np.any(valid):
        with np.errstate(divide="ignore", invalid="ignore"):
            pmi = np.log(pij[valid] / pi_outer[valid])
            denom = -np.log(pij[valid])
            vals = pmi / denom
        npmi[valid] = vals

    npmi = np.clip(npmi, -1.0, 1.0)
    return npmi


def main() -> int:
    args = _parse_args()
    output_path = args.output if args.output is not None else args.input.parent / "npmi.npy"

    label_counts, pair_counts, label_columns, n_docs = _load_counts(
        csv_path=args.input, positive_threshold=args.positive_threshold
    )
    npmi = _compute_npmi(label_counts=label_counts, pair_counts=pair_counts, n_docs=n_docs)
    np.fill_diagonal(npmi, 1.0)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(output_path, npmi.astype(np.float32))

    print(f"input: {args.input}")
    print(f"output: {output_path}")
    print(f"docs: {n_docs}")
    print(f"labels: {len(label_columns)}")
    print(f"shape: {npmi.shape}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
