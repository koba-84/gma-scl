from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from datasets import DatasetDict, load_dataset, load_from_disk
from transformers import AutoTokenizer

from src.data.components.hf_tokenized_dataset import TokenizedDatasetBundle


def _read_csv_schema(train_csv: Path) -> tuple[str, list[str]]:
    """Read text/label schema from train CSV header."""
    with train_csv.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
    if header is None or len(header) < 2:
        raise ValueError(f"Invalid CSV in {train_csv}: expected text + at least one label column.")
    text_column = header[0].strip()
    label_columns = [col.strip() for col in header[1:]]
    return text_column, label_columns


def _cache_key(
    dataset_name: str, tokenizer_name: str, max_length: int, label_columns: list[str]
) -> str:
    """Build deterministic cache key for preprocessing configuration."""
    payload = {
        "dataset_name": dataset_name,
        "tokenizer_name": tokenizer_name,
        "max_length": int(max_length),
        "label_columns": label_columns,
    }
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    return digest[:16]


def _dataset_files(data_dir: str | Path, dataset_name: str) -> dict[str, Path]:
    dataset_dir = Path(data_dir) / dataset_name
    return {
        "train": dataset_dir / "train.csv",
        "validation": dataset_dir / "dev.csv",
        "test": dataset_dir / "test.csv",
    }


def _cache_paths(
    cache_dir: str | Path,
    dataset_name: str,
    tokenizer_name: str,
    max_length: int,
    label_columns: list[str],
) -> tuple[Path, Path]:
    key = _cache_key(dataset_name, tokenizer_name, max_length, label_columns)
    cache_path = Path(cache_dir) / dataset_name / key
    metadata_path = cache_path / "metadata.json"
    return cache_path, metadata_path


def _expected_metadata(
    dataset_name: str,
    tokenizer_name: str,
    max_length: int,
    label_columns: list[str],
    text_column: str,
) -> dict[str, object]:
    return {
        "dataset_name": dataset_name,
        "tokenizer_name": tokenizer_name,
        "max_length": int(max_length),
        "label_columns": label_columns,
        "text_column": text_column,
    }


def _apply_torch_format(dataset_dict: DatasetDict) -> DatasetDict:
    torch_columns = ["input_ids", "attention_mask", "labels", "is_empty_text"]
    dataset_dict.set_format(
        type="torch",
        columns=torch_columns,
        output_all_columns=True,
    )
    return dataset_dict
def _tokenize_dataset_dict(
    data_dir: str,
    dataset_name: str,
    tokenizer_name: str,
    max_length: int,
    num_proc: int,
) -> tuple[DatasetDict, list[str], str]:
    data_files = _dataset_files(data_dir=data_dir, dataset_name=dataset_name)
    for path in data_files.values():
        if not path.exists():
            raise FileNotFoundError(f"Dataset file not found: {path}")

    text_column, label_columns = _read_csv_schema(data_files["train"])
    raw = load_dataset(
        "csv",
        data_files={split: str(path) for split, path in data_files.items()},
    )
    required_columns = [text_column, *label_columns]
    for split_name, split_ds in raw.items():
        split_columns = set(split_ds.column_names)
        for column in required_columns:
            if column not in split_columns:
                raise ValueError(f"Missing label column '{column}' in {split_name} split.")
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, use_fast=True)

    def preprocess(batch: dict[str, list[object]]) -> dict[str, object]:
        texts = [str(v) for v in batch[text_column]]
        is_empty_text = []
        for text in texts:
            stripped = text.strip()
            is_empty_text.append(stripped == "" or stripped.lower() == "nan")
        tokenized = tokenizer(
            texts,
            truncation=True,
            padding="max_length",
            max_length=max_length,
        )
        labels = []
        rows = len(texts)
        for i in range(rows):
            row_labels: list[float] = []
            for col in label_columns:
                value = batch[col][i]
                if value is None:
                    raise ValueError(f"Missing label column '{col}'")
                if not isinstance(value, int | float | str):
                    raise ValueError(
                        f"Invalid label value type for '{col}': {type(value).__name__}"
                    )
                row_labels.append(float(value))
            labels.append(row_labels)
        tokenized["labels"] = labels
        tokenized["is_empty_text"] = is_empty_text
        tokenized[text_column] = texts
        return tokenized

    dataset_dict = raw.map(
        preprocess,
        batched=True,
        num_proc=max(1, int(num_proc)),
        remove_columns=raw["train"].column_names,
        desc="Tokenizing dataset",
    )
    return dataset_dict, label_columns, text_column


def materialize_tokenized_splits_cache(
    data_dir: str,
    dataset_name: str,
    tokenizer_name: str,
    max_length: int,
    cache_dir: str,
    num_proc: int,
) -> None:
    """Ensure tokenized split cache exists on disk for the requested preprocessing config."""
    data_files = _dataset_files(data_dir=data_dir, dataset_name=dataset_name)
    for path in data_files.values():
        if not path.exists():
            raise FileNotFoundError(f"Dataset file not found: {path}")

    text_column, label_columns = _read_csv_schema(data_files["train"])
    cache_path, metadata_path = _cache_paths(
        cache_dir=cache_dir,
        dataset_name=dataset_name,
        tokenizer_name=tokenizer_name,
        max_length=max_length,
        label_columns=label_columns,
    )
    expected_metadata = _expected_metadata(
        dataset_name=dataset_name,
        tokenizer_name=tokenizer_name,
        max_length=max_length,
        label_columns=label_columns,
        text_column=text_column,
    )

    if cache_path.exists() and metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if metadata == expected_metadata:
            return

    tokenized, _, _ = _tokenize_dataset_dict(
        data_dir=data_dir,
        dataset_name=dataset_name,
        tokenizer_name=tokenizer_name,
        max_length=max_length,
        num_proc=num_proc,
    )
    cache_path.mkdir(parents=True, exist_ok=True)
    tokenized.save_to_disk(str(cache_path))
    metadata_path.write_text(
        json.dumps(expected_metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def load_tokenized_dataset_bundle(
    data_dir: str,
    dataset_name: str,
    tokenizer_name: str,
    max_length: int,
    cache_dir: str,
) -> TokenizedDatasetBundle:
    """Load cached tokenized splits and schema as a bundle."""
    train_csv = _dataset_files(data_dir=data_dir, dataset_name=dataset_name)["train"]
    text_column, label_columns = _read_csv_schema(train_csv)
    cache_path, metadata_path = _cache_paths(
        cache_dir=cache_dir,
        dataset_name=dataset_name,
        tokenizer_name=tokenizer_name,
        max_length=max_length,
        label_columns=label_columns,
    )
    if not cache_path.exists() or not metadata_path.exists():
        raise FileNotFoundError(f"Tokenized cache not found: {cache_path}")

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    expected_metadata = _expected_metadata(
        dataset_name=dataset_name,
        tokenizer_name=tokenizer_name,
        max_length=max_length,
        label_columns=label_columns,
        text_column=text_column,
    )
    if metadata != expected_metadata:
        raise RuntimeError(f"Tokenized cache metadata mismatch: {cache_path}")

    dataset_dict = load_from_disk(str(cache_path))
    if not isinstance(dataset_dict, DatasetDict):
        raise RuntimeError(f"Cache at {cache_path} is not a DatasetDict.")
    dataset_dict = _apply_torch_format(dataset_dict)
    return TokenizedDatasetBundle(
        dataset_dict=dataset_dict,
        label_columns=label_columns,
        text_column=text_column,
    )
