from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest

from src.data.classification_datamodule import ClassificationDataModule
from src.data.contrastive_datamodule import ContrastiveDataModule


def write_synthetic_multilabel_dataset(data_root: Path, dataset_name: str = "aapd") -> None:
    dataset_dir = data_root / dataset_name
    dataset_dir.mkdir(parents=True, exist_ok=True)

    def _write_split(name: str, rows: list[str]) -> None:
        (dataset_dir / name).write_text(
            "text,label_a,label_b\n" + "".join(rows),
            encoding="utf-8",
        )

    _write_split(
        "train.csv",
        [
            "train sample 1,1,0\n",
            "train sample 2,0,1\n",
            "train sample 3,1,1\n",
            ",0,0\n",
        ],
    )
    _write_split(
        "dev.csv",
        [
            "dev sample 1,1,0\n",
            "dev sample 2,0,1\n",
        ],
    )
    _write_split(
        "test.csv",
        [
            "test sample 1,1,1\n",
            "test sample 2,0,0\n",
        ],
    )


def write_label_descriptions_json(
    data_root: Path,
    dataset_name: str,
    descriptions: list[str],
) -> Path:
    dataset_dir = data_root / dataset_name
    dataset_dir.mkdir(parents=True, exist_ok=True)
    (dataset_dir / "label_descriptions.json").write_text(
        json.dumps(
            {
                "labels": [
                    {"index": index, "description": description}
                    for index, description in enumerate(descriptions, start=1)
                ]
            }
        ),
        encoding="utf-8",
    )
    return dataset_dir


@pytest.fixture(scope="function")
def synthetic_multilabel_dataset_factory(tmp_path: Path):
    def _build(
        *,
        train_rows: list[str] | None = None,
        dev_rows: list[str] | None = None,
        test_rows: list[str] | None = None,
    ) -> tuple[Path, Path]:
        data_root = tmp_path / "data"
        dataset_name = "aapd"
        write_synthetic_multilabel_dataset(data_root=data_root, dataset_name=dataset_name)
        dataset_dir = data_root / dataset_name

        if train_rows is not None:
            (dataset_dir / "train.csv").write_text(
                "text,label_a,label_b\n" + "".join(train_rows),
                encoding="utf-8",
            )
        if dev_rows is not None:
            (dataset_dir / "dev.csv").write_text(
                "text,label_a,label_b\n" + "".join(dev_rows),
                encoding="utf-8",
            )
        if test_rows is not None:
            (dataset_dir / "test.csv").write_text(
                "text,label_a,label_b\n" + "".join(test_rows),
                encoding="utf-8",
            )
        return data_root, dataset_dir

    return _build


@pytest.fixture(scope="function")
def synthetic_multilabel_dataset(
    synthetic_multilabel_dataset_factory,
) -> tuple[Path, Path]:
    return synthetic_multilabel_dataset_factory()


@pytest.fixture(scope="function")
def classification_dm_factory(
    synthetic_multilabel_dataset: tuple[Path, Path],
    tmp_path: Path,
):
    data_root, _ = synthetic_multilabel_dataset

    def _build(**kwargs: Any) -> ClassificationDataModule:
        defaults = {
            "data_dir": str(data_root),
            "dataset_name": "aapd",
            "batch_size": 2,
            "num_workers": 0,
            "pin_memory": False,
            "hf_cache_dir": str(tmp_path / "hf_cache"),
        }
        defaults.update(kwargs)
        return ClassificationDataModule(**cast(Any, defaults))

    return _build


@pytest.fixture(scope="function")
def classification_dm_builder(tmp_path: Path):
    def _build(
        data_root: Path, *, dataset_name: str = "aapd", **kwargs: Any
    ) -> ClassificationDataModule:
        defaults = {
            "data_dir": str(data_root),
            "dataset_name": dataset_name,
            "batch_size": 2,
            "num_workers": 0,
            "pin_memory": False,
            "hf_cache_dir": str(tmp_path / "hf_cache"),
        }
        defaults.update(kwargs)
        return ClassificationDataModule(**cast(Any, defaults))

    return _build


@pytest.fixture(scope="function")
def contrastive_dm_factory(
    synthetic_multilabel_dataset: tuple[Path, Path],
    tmp_path: Path,
):
    data_root, _ = synthetic_multilabel_dataset

    def _build(**kwargs: Any) -> ContrastiveDataModule:
        defaults = {
            "data_dir": str(data_root),
            "dataset_name": "aapd",
            "batch_size": 2,
            "num_workers": 0,
            "pin_memory": False,
            "hf_cache_dir": str(tmp_path / "hf_cache"),
        }
        defaults.update(kwargs)
        return ContrastiveDataModule(**cast(Any, defaults))

    return _build
