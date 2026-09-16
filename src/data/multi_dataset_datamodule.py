from __future__ import annotations

from bisect import bisect_right
from collections.abc import Mapping, Sequence, Sized
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import rootutils
import torch
from lightning import LightningDataModule
from torch.utils.data import DataLoader, Dataset

rootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)

from src.data.components.hf_tokenized_dataset import TokenizedTorchDataset
from src.data.tokenized_dataset_cache import (
    load_tokenized_dataset_bundle,
    materialize_tokenized_splits_cache,
)

BatchInput = dict[str, torch.Tensor]
SingleDatasetItem = tuple[BatchInput, torch.Tensor, str]
BatchType = tuple[BatchInput, torch.Tensor]


@dataclass(frozen=True)
class MultiDatasetSpec:
    """Schema and global-label offset for one configured dataset."""

    name: str
    dataset_id: int
    label_columns: tuple[str, ...]
    label_offset: int

    @property
    def num_classes(self) -> int:
        return len(self.label_columns)

    @property
    def label_slice(self) -> slice:
        return slice(self.label_offset, self.label_offset + self.num_classes)


class MultiDatasetSampleDataset(Dataset[tuple[BatchInput, torch.Tensor, int, str]]):
    """Concatenate tokenized datasets while preserving local dataset identity."""

    def __init__(
        self,
        datasets: Sequence[Dataset[SingleDatasetItem]],
        specs: Sequence[MultiDatasetSpec],
    ) -> None:
        if len(datasets) != len(specs) or not datasets:
            raise ValueError("datasets and specs must be non-empty and have equal length.")
        self.datasets = list(datasets)
        self.specs = list(specs)
        self.total_num_classes = sum(spec.num_classes for spec in self.specs)
        self._cumulative_sizes: list[int] = []
        total = 0
        for dataset in self.datasets:
            total += len(cast(Sized, dataset))
            self._cumulative_sizes.append(total)

    def __len__(self) -> int:
        return self._cumulative_sizes[-1]

    def _resolve_index(self, index: int) -> tuple[int, int]:
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError(f"index out of range: {index}")
        dataset_id = bisect_right(self._cumulative_sizes, index)
        previous_size = 0 if dataset_id == 0 else self._cumulative_sizes[dataset_id - 1]
        return dataset_id, index - previous_size

    def __getitem__(self, index: int) -> tuple[BatchInput, torch.Tensor, int, str]:
        dataset_id, local_index = self._resolve_index(index)
        features, local_labels, text = self.datasets[dataset_id][local_index]
        if local_labels.ndim != 1 or local_labels.size(0) != self.specs[dataset_id].num_classes:
            raise ValueError(
                f"Dataset '{self.specs[dataset_id].name}' label shape mismatch: "
                f"expected [{self.specs[dataset_id].num_classes}], got {tuple(local_labels.shape)}"
            )
        global_labels = torch.zeros(self.total_num_classes, dtype=torch.float32)
        spec = self.specs[dataset_id]
        global_labels[spec.label_slice] = local_labels.to(dtype=torch.float32)
        return features, global_labels, dataset_id, text


def _collate_multi_dataset(
    batch: list[tuple[BatchInput, torch.Tensor, int, str]],
) -> BatchType:
    if not batch:
        raise ValueError("Cannot collate an empty multi-dataset batch.")
    inputs = {
        "input_ids": torch.stack([item[0]["input_ids"] for item in batch], dim=0),
        "attention_mask": torch.stack([item[0]["attention_mask"] for item in batch], dim=0),
        "empty_text_mask": torch.stack([item[0]["empty_text_mask"] for item in batch], dim=0),
        "dataset_id": torch.tensor([item[2] for item in batch], dtype=torch.long),
    }
    labels = torch.stack([item[1] for item in batch], dim=0)
    return inputs, labels


class MultiDatasetDataModule(LightningDataModule):
    """Tokenized datamodule that randomly mixes multiple dataset label spaces."""

    def __init__(
        self,
        data_dir: str = "data/",
        dataset_names: list[str] | tuple[str, ...] = (),
        dataset_num_classes: Mapping[str, int] | None = None,
        batch_size: int = 64,
        num_workers: int = 0,
        pin_memory: bool = False,
        seed: int | None = None,
        drop_last: bool = False,
        tokenizer_name: str = "roberta-base",
        max_length: int = 512,
        hf_cache_dir: str = "tmp/hf_cache",
        hf_num_proc: int = 1,
    ) -> None:
        super().__init__()
        names = [str(name) for name in dataset_names]
        if not names or len(set(names)) != len(names):
            raise ValueError("dataset_names must contain unique dataset names.")
        self.save_hyperparameters(logger=False)
        self.dataset_specs: tuple[MultiDatasetSpec, ...] = ()
        self.data_train: MultiDatasetSampleDataset | None = None
        self.data_val: MultiDatasetSampleDataset | None = None
        self.data_test: MultiDatasetSampleDataset | None = None
        self.batch_size_per_device = int(batch_size)

    @property
    def num_classes(self) -> int:
        return sum(spec.num_classes for spec in self.dataset_specs)

    @property
    def num_classes_by_dataset(self) -> dict[str, int]:
        return {spec.name: spec.num_classes for spec in self.dataset_specs}

    @property
    def dataset_id_by_name(self) -> dict[str, int]:
        return {spec.name: spec.dataset_id for spec in self.dataset_specs}

    @property
    def label_slices(self) -> dict[str, slice]:
        return {spec.name: spec.label_slice for spec in self.dataset_specs}

    def _hparams_map(self) -> Mapping[str, object]:
        return cast(Mapping[str, object], self.hparams)

    def _hparam_int(self, key: str) -> int:
        return int(cast(int | str, self._hparams_map()[key]))

    def _hparam_bool(self, key: str) -> bool:
        return bool(self._hparams_map()[key])

    def _dataset_names(self) -> list[str]:
        raw = self._hparams_map().get("dataset_names")
        if not isinstance(raw, Sequence) or isinstance(raw, str):
            raise ValueError("dataset_names must be a non-empty sequence.")
        return [str(name) for name in raw]

    def _prepare_dataset(self, dataset_name: str) -> None:
        materialize_tokenized_splits_cache(
            data_dir=str(self._hparams_map()["data_dir"]),
            dataset_name=dataset_name,
            tokenizer_name=str(self._hparams_map()["tokenizer_name"]),
            max_length=self._hparam_int("max_length"),
            cache_dir=str(self._hparams_map()["hf_cache_dir"]),
            num_proc=self._hparam_int("hf_num_proc"),
        )

    def prepare_data(self) -> None:
        """Materialize tokenized caches for every configured dataset."""
        for dataset_name in self._dataset_names():
            self._prepare_dataset(dataset_name)

    def _configure_batch_size_per_device(self) -> None:
        if self.trainer is None:
            return
        world_size = int(self.trainer.world_size)
        batch_size = self._hparam_int("batch_size")
        if batch_size % world_size != 0:
            raise RuntimeError(
                f"Batch size ({batch_size}) is not divisible by world size ({world_size})."
            )
        self.batch_size_per_device = batch_size // world_size

    def setup(self, stage: str | None = None) -> None:
        """Load all tokenized splits and validate their local label schemas."""
        self._configure_batch_size_per_device()
        if self.data_train is not None:
            return
        data_dir = str(self._hparams_map()["data_dir"])
        tokenizer_name = str(self._hparams_map()["tokenizer_name"])
        max_length = self._hparam_int("max_length")
        cache_dir = str(self._hparams_map()["hf_cache_dir"])
        bundles = []
        for dataset_name in self._dataset_names():
            self._prepare_dataset(dataset_name)
            bundles.append(
                load_tokenized_dataset_bundle(
                    data_dir=data_dir,
                    dataset_name=dataset_name,
                    tokenizer_name=tokenizer_name,
                    max_length=max_length,
                    cache_dir=cache_dir,
                )
            )

        specs: list[MultiDatasetSpec] = []
        offset = 0
        configured_counts = self._hparams_map().get("dataset_num_classes") or {}
        for dataset_id, (dataset_name, bundle) in enumerate(zip(self._dataset_names(), bundles)):
            spec = MultiDatasetSpec(
                name=dataset_name,
                dataset_id=dataset_id,
                label_columns=tuple(bundle.label_columns),
                label_offset=offset,
            )
            expected_count = (
                configured_counts.get(dataset_name)
                if isinstance(configured_counts, Mapping)
                else None
            )
            if (
                expected_count is not None
                and int(cast(int | str, expected_count)) != spec.num_classes
            ):
                raise ValueError(
                    f"dataset_num_classes mismatch for '{dataset_name}': "
                    f"config={expected_count}, dataset={spec.num_classes}"
                )
            specs.append(spec)
            offset += spec.num_classes
        self.dataset_specs = tuple(specs)

        split_datasets: dict[str, list[Dataset[SingleDatasetItem]]] = {
            "train": [],
            "validation": [],
            "test": [],
        }
        for spec, bundle in zip(self.dataset_specs, bundles):
            for split_name in split_datasets:
                split_datasets[split_name].append(
                    TokenizedTorchDataset(
                        bundle.dataset_dict[split_name],
                        text_column=bundle.text_column,
                    )
                )
        self.data_train = MultiDatasetSampleDataset(split_datasets["train"], self.dataset_specs)
        self.data_val = MultiDatasetSampleDataset(split_datasets["validation"], self.dataset_specs)
        self.data_test = MultiDatasetSampleDataset(split_datasets["test"], self.dataset_specs)

    def _require_dataset(self, split: str) -> MultiDatasetSampleDataset:
        dataset = {"train": self.data_train, "val": self.data_val, "test": self.data_test}.get(
            split
        )
        if dataset is None:
            raise RuntimeError(f"data_{split} is not initialized. Call setup() first.")
        return dataset

    def _build_dataloader(
        self,
        split: str,
        shuffle: bool,
        drop_last: bool | None = None,
    ) -> DataLoader:
        if drop_last is None:
            drop_last = self._hparam_bool("drop_last") if split == "train" else False
        return DataLoader(
            self._require_dataset(split),
            batch_size=self.batch_size_per_device,
            shuffle=shuffle,
            num_workers=self._hparam_int("num_workers"),
            pin_memory=self._hparam_bool("pin_memory"),
            drop_last=drop_last,
            collate_fn=_collate_multi_dataset,
        )

    def train_dataloader(self) -> DataLoader:
        """Return a randomly mixed train dataloader."""
        return self._build_dataloader("train", shuffle=True)

    def covariance_dataloader(self) -> DataLoader:
        """Return every training sample once for epoch-level covariance refresh."""
        return self._build_dataloader("train", shuffle=False, drop_last=False)

    def val_dataloader(self) -> DataLoader:
        """Return the combined validation dataloader."""
        return self._build_dataloader("val", shuffle=False)

    def test_dataloader(self) -> DataLoader:
        """Return the combined test dataloader."""
        return self._build_dataloader("test", shuffle=False)


__all__ = [
    "MultiDatasetDataModule",
    "MultiDatasetSampleDataset",
    "MultiDatasetSpec",
    "_collate_multi_dataset",
]
