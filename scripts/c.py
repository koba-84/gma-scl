from pathlib import Path

import pandas as pd  # type: ignore[import-untyped]
import torch
from torchmetrics.classification import MultilabelF1Score

TRAIN_CSV_PATH = Path("data/uklex/train.csv")
PREDICTION_DIR = Path("tmp/pred/uklex")
MODEL_NAMES = ["bce", "base", "mulsupcon", "gma_scl"]
NUM_BANDS = 2


def load_label_frequency() -> pd.Series:
    df = pd.read_csv(TRAIN_CSV_PATH)
    label_df = df.drop(columns=["abstract"])
    return (label_df == 1).sum()


def build_rank_order(label_freq: pd.Series) -> pd.Series:
    ordered_index = label_freq.sort_values(ascending=False, kind="stable").index
    rank_order = pd.Series(
        data=range(1, len(ordered_index) + 1),
        index=ordered_index,
        dtype="int64",
    )
    return rank_order.reindex(label_freq.index)


def band_label(index: int) -> str:
    return f"half_{index + 1}"


def build_frequency_bands(
    label_freq: pd.Series,
    rank_order: pd.Series,
) -> tuple[pd.Series, list[str], dict[str, str]]:
    ordered_labels = rank_order.sort_values(kind="stable").index.to_list()
    base_size, remainder = divmod(len(ordered_labels), NUM_BANDS)
    labels = [band_label(index) for index in range(NUM_BANDS)]
    band_map = pd.Series(index=label_freq.index, dtype="object")

    start = 0
    for index, label in enumerate(labels):
        size = base_size + (1 if index < remainder else 0)
        band_labels = ordered_labels[start : start + size]
        band_map.loc[band_labels] = label
        start += size

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
    label_freq = load_label_frequency()
    rank_order = build_rank_order(label_freq)
    band_map, band_labels, band_ranges = build_frequency_bands(label_freq, rank_order)

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
    print("UKLEX 1/2 frequency bands")
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
