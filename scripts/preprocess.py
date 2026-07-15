#!/usr/bin/env python3
"""Split *_train.txt into train/val with 8:2 ratio."""

import argparse
import os
import random
import sys
from pathlib import Path

RATIO = 0.8


def split_file(src: Path, seed: int) -> None:
    if not src.is_file():
        raise FileNotFoundError(f"not found: {src}")

    dst_train = src.with_name("train.txt")
    dst_val = src.with_name("val.txt")

    tmp_train = dst_train.with_suffix(".txt.tmp")
    tmp_val = dst_val.with_suffix(".txt.tmp")

    # clean any leftovers before starting
    for p in (tmp_train, tmp_val, dst_train, dst_val):
        if p.exists():
            p.unlink()

    try:
        lines = src.read_text(encoding="utf-8").splitlines()
        rng = random.Random(seed)
        rng.shuffle(lines)
        cut = int(len(lines) * RATIO)
        train_lines = lines[:cut]
        val_lines = lines[cut:]

        tmp_train.write_text(
            "\n".join(train_lines) + ("\n" if train_lines else ""), encoding="utf-8"
        )
        tmp_val.write_text("\n".join(val_lines) + ("\n" if val_lines else ""), encoding="utf-8")

        os.replace(tmp_train, dst_train)
        os.replace(tmp_val, dst_val)
    except Exception:
        # remove partials and retry once
        for p in (tmp_train, tmp_val, dst_train, dst_val):
            if p.exists():
                p.unlink()
        # retry with same seed for determinism
        lines = src.read_text(encoding="utf-8").splitlines()
        rng = random.Random(seed)
        rng.shuffle(lines)
        cut = int(len(lines) * RATIO)
        train_lines = lines[:cut]
        val_lines = lines[cut:]

        tmp_train.write_text(
            "\n".join(train_lines) + ("\n" if train_lines else ""), encoding="utf-8"
        )
        tmp_val.write_text("\n".join(val_lines) + ("\n" if val_lines else ""), encoding="utf-8")

        os.replace(tmp_train, dst_train)
        os.replace(tmp_val, dst_val)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--glob",
        default="data/*/_train.txt",
        help="glob pattern for input _train.txt files",
    )
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    paths = sorted(Path().glob(args.glob))
    if not paths:
        print(f"no files matched: {args.glob}", file=sys.stderr)
        return 1

    for src in paths:
        split_file(src, args.seed)
        print(f"split: {src} -> {src.with_name('train.txt')}, {src.with_name('val.txt')}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
