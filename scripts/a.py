import argparse
from pathlib import Path

import pandas as pd  # type: ignore[import-untyped]
import torch
from torchmetrics.classification import MultilabelF1Score

TRAIN_CSV_PATH = Path("data/aapd/train.csv")
PREDICTION_DIR = Path("tmp/pred/aapd")
MODEL_NAMES = ["bce", "base", "mulsupcon", "gma_scl"]


def load_label_frequency() -> pd.Series:
    df = pd.read_csv(TRAIN_CSV_PATH)
    label_df = df.drop(columns=["abstract"])
    return (label_df == 1).sum()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report overall and rank-based frequency-band macro-F1 from saved AAPD predictions."
    )
    parser.add_argument(
        "--rank-boundaries",
        type=int,
        nargs="*",
        default=None,
        help="Exactly three sorted rank boundaries. Bands become 1-b1, (b1+1)-b2, (b2+1)-b3, (b3+1)-N.",
    )
    return parser.parse_args()


def default_rank_boundaries(num_labels: int) -> list[int]:
    default_boundaries = [6, 22, 38]
    return validate_rank_boundaries(default_boundaries, num_labels)


def validate_rank_boundaries(rank_boundaries: list[int], num_labels: int) -> list[int]:
    if len(rank_boundaries) != 3:
        raise ValueError("rank boundaries must contain exactly three values to form four bands")
    if any(boundary <= 0 for boundary in rank_boundaries):
        raise ValueError("rank boundaries must be positive integers")
    if any(boundary >= num_labels for boundary in rank_boundaries):
        raise ValueError("rank boundaries must be smaller than the number of labels")
    if rank_boundaries != sorted(rank_boundaries):
        raise ValueError("rank boundaries must be sorted in ascending order")
    if len(set(rank_boundaries)) != len(rank_boundaries):
        raise ValueError("rank boundaries must not contain duplicates")
    return rank_boundaries


def build_rank_order(label_freq: pd.Series) -> pd.Series:
    ordered_index = label_freq.sort_values(ascending=False, kind="stable").index
    rank_order = pd.Series(
        data=range(1, len(ordered_index) + 1),
        index=ordered_index,
        dtype="int64",
    )
    return rank_order.reindex(label_freq.index)


def band_label(lower_rank: int | None, upper_rank: int | None) -> str:
    if lower_rank is None and upper_rank is None:
        return "all"
    if lower_rank is None:
        return f"rank_1_{upper_rank}"
    if upper_rank is None:
        return f"rank_{lower_rank + 1}_plus"
    return f"rank_{lower_rank + 1}_{upper_rank}"


def build_rank_bands(
    label_freq: pd.Series,
    rank_order: pd.Series,
    rank_boundaries: list[int],
) -> tuple[pd.Series, list[str], dict[str, str]]:
    bins = [0, *rank_boundaries, len(label_freq)]
    labels = [
        band_label(None if index == 0 else rank_boundaries[index - 1], upper_rank)
        for index, upper_rank in enumerate([*rank_boundaries, None])
    ]
    band_ids = pd.cut(rank_order, bins=bins, labels=labels, include_lowest=True, right=True)
    band_map = pd.Series(band_ids, index=label_freq.index, dtype="object")

    band_ranges = {}
    for label in labels:
        band_freq = label_freq[band_map == label]
        band_rank = rank_order[band_map == label]
        if band_freq.empty:
            band_ranges[label] = "rank=[], n=0, freq=[]"
            continue
        band_ranges[label] = (
            f"rank=[{int(band_rank.min())}, {int(band_rank.max())}], "
            f"n={len(band_freq)}, freq=[{int(band_freq.min())}, {int(band_freq.max())}]"
        )
    return band_map, labels, band_ranges


def macro_f1(scores: torch.Tensor, targets: torch.Tensor) -> float:
    if scores.shape[1] == 0:
        return float("nan")
    metric = MultilabelF1Score(num_labels=scores.shape[1], average="macro", threshold=0.5)
    return float(metric(scores.float(), targets.int()).item())


def evaluate_prediction_file(
    prediction_path: Path,
    band_map: pd.Series,
    band_labels: list[str],
) -> dict[str, float]:
    payload = torch.load(prediction_path, map_location="cpu", weights_only=False)
    scores = payload["scores"]
    targets = payload["targets"]

    if scores.shape != targets.shape:
        raise ValueError(f"shape mismatch: {prediction_path} -> {scores.shape} != {targets.shape}")
    if scores.shape[1] != len(band_map):
        raise ValueError(
            f"label count mismatch: {prediction_path} -> {scores.shape[1]} != {len(band_map)}"
        )

    result = {"overall_macro_f1": macro_f1(scores, targets)}
    for band in band_labels:
        band_mask = torch.tensor((band_map == band).to_numpy(), dtype=torch.bool)
        band_scores = scores[:, band_mask]
        band_targets = targets[:, band_mask]
        result[band] = macro_f1(band_scores, band_targets)
    return result


def seed_suffix(prediction_path: Path, model_name: str) -> int | None:
    suffix = prediction_path.stem[len(model_name) :]
    if not suffix.isdigit():
        return None
    return int(suffix)


def discover_prediction_files(model_name: str) -> list[tuple[int, Path]]:
    candidates: list[tuple[int, Path]] = []
    for prediction_path in PREDICTION_DIR.glob(f"{model_name}*.pt"):
        seed = seed_suffix(prediction_path, model_name)
        if seed is not None:
            candidates.append((seed, prediction_path))
    if not candidates:
        raise FileNotFoundError(
            f"no prediction artifacts found for {model_name}: expected files like "
            f"{PREDICTION_DIR / f'{model_name}0.pt'}"
        )
    return sorted(candidates, key=lambda item: item[0])


def evaluate_model_predictions(
    model_name: str,
    band_map: pd.Series,
    band_labels: list[str],
) -> tuple[list[dict[str, float | int | str]], dict[str, float | int]]:
    prediction_paths = discover_prediction_files(model_name)
    per_seed_rows: list[dict[str, float | int | str]] = []
    for seed, prediction_path in prediction_paths:
        per_seed_rows.append(
            {
                "model": model_name,
                "seed": seed,
                **evaluate_prediction_file(prediction_path, band_map, band_labels),
            }
        )
    mean_metrics = pd.DataFrame(per_seed_rows).drop(columns=["model", "seed"]).mean().to_dict()
    return per_seed_rows, {"seed_count": len(prediction_paths), **mean_metrics}


def main() -> None:
    args = parse_args()
    label_freq = load_label_frequency()
    rank_order = build_rank_order(label_freq)
    rank_boundaries = (
        default_rank_boundaries(len(label_freq))
        if args.rank_boundaries is None or len(args.rank_boundaries) == 0
        else validate_rank_boundaries(args.rank_boundaries, len(label_freq))
    )
    band_map, band_labels, band_ranges = build_rank_bands(label_freq, rank_order, rank_boundaries)

    per_seed_rows = []
    average_rows = {}
    for model_name in MODEL_NAMES:
        model_seed_rows, average_rows[model_name] = evaluate_model_predictions(
            model_name, band_map, band_labels
        )
        per_seed_rows.extend(model_seed_rows)

    per_seed_summary = pd.DataFrame(per_seed_rows).set_index(["model", "seed"])
    per_seed_summary = per_seed_summary[["overall_macro_f1", *band_labels]]
    average_summary = pd.DataFrame.from_dict(average_rows, orient="index")
    average_summary = average_summary[["seed_count", "overall_macro_f1", *band_labels]]
    print(f"Rank boundaries: {rank_boundaries}")
    print("Rank-based frequency bands")
    for band in band_labels:
        print(f"- {band}: {band_ranges[band]}")
    print()
    print("Per-seed Macro-F1 by model")
    print(per_seed_summary.to_string(float_format=lambda value: f"{value:.4f}"))
    print()
    print("Average Macro-F1 by model")
    print(average_summary.to_string(float_format=lambda value: f"{value:.4f}"))


if __name__ == "__main__":
    main()
