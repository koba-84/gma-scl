from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import cast

import rootutils
import torch
from lightning import LightningDataModule
from torch.utils.data import DataLoader, Dataset, Sampler

rootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)

from src.data.components.hf_tokenized_dataset import TokenizedTorchDataset
from src.data.tokenized_dataset_cache import (
    load_tokenized_dataset_bundle,
    materialize_tokenized_splits_cache,
)

BatchInput = dict[str, torch.Tensor]
BatchTuple = tuple[BatchInput, torch.Tensor]
TokenizedDataset = Dataset[tuple[BatchInput, torch.Tensor, str]]
BatchCollate = Callable[[list[tuple[BatchInput, torch.Tensor, str]]], object]


class TokenizedCSVDataModuleBase(LightningDataModule):
    """Shared LightningDataModule base for tokenized CSV datasets."""

    def __init__(self, batch_size: int) -> None:
        super().__init__()
        self.data_train: TokenizedDataset | None = None
        self.data_val: TokenizedDataset | None = None
        self.data_test: TokenizedDataset | None = None
        self._label2id: dict[str, int] = {}
        self._id2label: dict[int, str] = {}
        self.batch_size_per_device = batch_size

    @property
    def num_classes(self) -> int:
        """Return the number of labels derived from the tokenized bundle schema."""
        return len(self._label2id)

    @property
    def label2id(self) -> dict[str, int]:
        """Return a copy of the label-to-index mapping."""
        return dict(self._label2id)

    @property
    def id2label(self) -> dict[int, str]:
        """Return a copy of the index-to-label mapping."""
        return dict(self._id2label)

    def _hparams_map(self) -> Mapping[str, object]:
        return cast(Mapping[str, object], self.hparams)

    def _hparam_int(self, key: str) -> int:
        return int(cast(int | str, self._hparams_map()[key]))

    def _hparam_bool(self, key: str) -> bool:
        return bool(self._hparams_map()[key])

    def _hparam_str(self, key: str) -> str:
        return str(self._hparams_map()[key])

    def prepare_data(self) -> None:
        """Materialize tokenized cache required before setup."""
        materialize_tokenized_splits_cache(
            data_dir=self._hparam_str("data_dir"),
            dataset_name=self._hparam_str("dataset_name"),
            tokenizer_name=self._hparam_str("tokenizer_name"),
            max_length=self._hparam_int("max_length"),
            cache_dir=self._hparam_str("hf_cache_dir"),
            num_proc=self._hparam_int("hf_num_proc"),
        )

    def _configure_batch_size_per_device(self) -> None:
        if self.trainer is None:
            return
        batch_size = self._hparam_int("batch_size")
        if batch_size % self.trainer.world_size != 0:
            raise RuntimeError(
                f"Batch size ({batch_size}) is not divisible by the number of devices ({self.trainer.world_size})."
            )
        self.batch_size_per_device = batch_size // self.trainer.world_size

    def _setup_tokenized_data(self) -> None:
        """Load cached tokenized splits and initialize shared dataset state."""
        self._configure_batch_size_per_device()
        if self.data_train or self.data_val or self.data_test:
            return

        materialize_tokenized_splits_cache(
            data_dir=self._hparam_str("data_dir"),
            dataset_name=self._hparam_str("dataset_name"),
            tokenizer_name=self._hparam_str("tokenizer_name"),
            max_length=self._hparam_int("max_length"),
            cache_dir=self._hparam_str("hf_cache_dir"),
            num_proc=self._hparam_int("hf_num_proc"),
        )
        bundle = load_tokenized_dataset_bundle(
            data_dir=self._hparam_str("data_dir"),
            dataset_name=self._hparam_str("dataset_name"),
            tokenizer_name=self._hparam_str("tokenizer_name"),
            max_length=self._hparam_int("max_length"),
            cache_dir=self._hparam_str("hf_cache_dir"),
        )

        self._label2id = {label: idx for idx, label in enumerate(bundle.label_columns)}
        self._id2label = {v: k for k, v in self._label2id.items()}
        self.data_train = TokenizedTorchDataset(bundle.dataset_dict["train"], text_column=bundle.text_column)
        self.data_val = TokenizedTorchDataset(
            bundle.dataset_dict["validation"], text_column=bundle.text_column
        )
        self.data_test = TokenizedTorchDataset(bundle.dataset_dict["test"], text_column=bundle.text_column)

    @staticmethod
    def _collate(batch: list[tuple[BatchInput, torch.Tensor, str]]) -> BatchTuple:
        inputs = {
            "input_ids": torch.stack([x[0]["input_ids"] for x in batch], dim=0),
            "attention_mask": torch.stack([x[0]["attention_mask"] for x in batch], dim=0),
            "empty_text_mask": torch.stack([x[0]["empty_text_mask"] for x in batch], dim=0),
        }
        labels = torch.stack([x[1] for x in batch], dim=0)
        return inputs, labels

    def _require_dataset(self, split: str) -> TokenizedDataset:
        datasets = {
            "train": self.data_train,
            "val": self.data_val,
            "test": self.data_test,
        }
        if split not in datasets:
            raise ValueError(f"Unsupported split: {split}")
        dataset = datasets[split]
        if dataset is None:
            raise RuntimeError(f"data_{split} is not initialized. Call setup() first.")
        return dataset

    def _build_dataloader(
        self,
        split: str,
        *,
        collate_fn: BatchCollate,
        shuffle: bool = False,
        sampler: Sampler[int] | None = None,
        batch_sampler: Sampler[list[int]] | None = None,
        drop_last: bool = False,
    ) -> DataLoader:
        dataset = self._require_dataset(split)
        if batch_sampler is not None:
            return DataLoader(
                dataset=dataset,
                batch_sampler=batch_sampler,
                num_workers=self._hparam_int("num_workers"),
                pin_memory=self._hparam_bool("pin_memory"),
                collate_fn=collate_fn,
            )
        return DataLoader(
            dataset=dataset,
            batch_size=self.batch_size_per_device,
            num_workers=self._hparam_int("num_workers"),
            pin_memory=self._hparam_bool("pin_memory"),
            shuffle=shuffle,
            sampler=sampler,
            drop_last=drop_last,
            collate_fn=collate_fn,
        )
