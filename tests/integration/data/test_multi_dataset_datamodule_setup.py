from dataclasses import dataclass

import pytest
import torch

import src.data.multi_dataset_datamodule as multi_dataset
from src.data.multi_dataset_datamodule import MultiDatasetDataModule


class _FakeSplit:
    def __init__(self, rows: list[dict[str, object]]) -> None:
        self.rows = rows

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, index: int) -> dict[str, object]:
        return self.rows[index]


@dataclass
class _FakeBundle:
    dataset_dict: dict[str, _FakeSplit]
    label_columns: list[str]
    text_column: str = "text"


def _fake_bundle(label_count: int, prefix: str) -> _FakeBundle:
    rows = []
    for index in range(2):
        rows.append(
            {
                "input_ids": torch.tensor([index, 1]),
                "attention_mask": torch.ones(2, dtype=torch.long),
                "is_empty_text": False,
                "labels": [float(index == 0)] * label_count,
                "text": f"{prefix}-{index}",
            }
        )
    return _FakeBundle(
        dataset_dict={
            "train": _FakeSplit(rows),
            "validation": _FakeSplit(rows[:1]),
            "test": _FakeSplit(rows[:1]),
        },
        label_columns=[f"{prefix}_{index}" for index in range(label_count)],
    )


def test_multi_dataset_datamodule_prepares_and_loads_all_splits(monkeypatch, tmp_path) -> None:
    prepared: list[str] = []
    bundles = {"a": _fake_bundle(2, "a"), "b": _fake_bundle(1, "b")}

    def _prepare(**kwargs: object) -> None:
        prepared.append(str(kwargs["dataset_name"]))

    monkeypatch.setattr(multi_dataset, "materialize_tokenized_splits_cache", _prepare)
    monkeypatch.setattr(
        multi_dataset,
        "load_tokenized_dataset_bundle",
        lambda **kwargs: bundles[str(kwargs["dataset_name"])],
    )

    datamodule = MultiDatasetDataModule(
        data_dir=str(tmp_path),
        dataset_names=["a", "b"],
        dataset_num_classes={"a": 2, "b": 1},
        batch_size=2,
        num_workers=0,
        pin_memory=False,
    )
    datamodule.prepare_data()
    datamodule.setup()

    assert prepared == ["a", "b", "a", "b"]
    assert datamodule.num_classes_by_dataset == {"a": 2, "b": 1}
    assert datamodule.dataset_id_by_name == {"a": 0, "b": 1}
    assert datamodule.label_slices == {"a": slice(0, 2), "b": slice(2, 3)}
    assert next(iter(datamodule.train_dataloader()))[1].shape == (2, 3)
    assert next(iter(datamodule.val_dataloader()))[1].shape == (2, 3)
    assert next(iter(datamodule.test_dataloader()))[1].shape == (2, 3)


def test_multi_dataset_datamodule_rejects_configured_label_count_mismatch(
    monkeypatch, tmp_path
) -> None:
    bundle = _fake_bundle(2, "a")
    monkeypatch.setattr(multi_dataset, "materialize_tokenized_splits_cache", lambda **_: None)
    monkeypatch.setattr(multi_dataset, "load_tokenized_dataset_bundle", lambda **_: bundle)
    datamodule = MultiDatasetDataModule(
        data_dir=str(tmp_path),
        dataset_names=["a"],
        dataset_num_classes={"a": 3},
    )

    with pytest.raises(ValueError, match="dataset_num_classes mismatch"):
        datamodule.setup()
