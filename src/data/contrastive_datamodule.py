from __future__ import annotations

import shutil
from collections.abc import Sequence, Sized
from pathlib import Path
from typing import cast

import rootutils
import torch
from torch.utils.data import DataLoader

rootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)

from src.data.components.dpp import DPPBatchSampler
from src.data.components.gcbs import GCBSSampler
from src.data.tokenized_datamodule_base import (
    BatchInput,
    TokenizedCSVDataModuleBase,
)

RefreshBatch = BatchInput


class ContrastiveDataModule(TokenizedCSVDataModuleBase):
    """LightningDataModule for supervised contrastive learning on tokenized CSV datasets."""

    def __init__(
        self,
        data_dir: str = "data/",
        dataset_name: str = "aapd",
        batch_size: int = 64,
        num_workers: int = 0,
        pin_memory: bool = False,
        seed: int | None = None,
        drop_last: bool = False,
        sampler_type: str = "shuffle",
        gcbs: dict[str, object] | None = None,
        dpp: dict[str, object] | None = None,
        tokenizer_name: str = "roberta-base",
        max_length: int = 512,
        hf_cache_dir: str = "tmp/hf_cache",
        hf_num_proc: int = 1,
    ) -> None:
        super().__init__(batch_size=batch_size)

        self.save_hyperparameters(logger=False)
        self.train_sampler: GCBSSampler | None = None
        self.train_batch_sampler: DPPBatchSampler | None = None

    def setup(self, stage: str | None = None) -> None:
        """Set up datasets, samplers, and runtime state for the stage."""
        self._setup_tokenized_data()
        train_dataset = self._require_dataset("train")

        sampler_type = self.get_sampler_type()
        if sampler_type == "gcbs":
            self.train_sampler = GCBSSampler(cast(Sized, train_dataset))
        if sampler_type == "dpp":
            dpp_cfg = self.get_sampler_config("dpp")
            mode = str(dpp_cfg.get("mode", "GS_bis"))
            random_state = cast(int | None, self._hparams_map().get("seed"))
            drop_last = bool(self._hparams_map().get("drop_last", False))
            self.train_batch_sampler = DPPBatchSampler(
                cast(Sized, train_dataset),
                batch_size=self.batch_size_per_device,
                drop_last=drop_last,
                mode=mode,
                random_state=random_state,
            )

    def get_sampler_type(self) -> str:
        """Return the normalized sampler type from config."""
        return str(self._hparams_map().get("sampler_type", "shuffle")).lower()

    def get_sampler_config(self, sampler_type: str | None = None) -> dict[str, object]:
        """Return configuration values for the selected sampler."""
        resolved_sampler = sampler_type or self.get_sampler_type()
        if resolved_sampler not in {"gcbs", "dpp"}:
            return {}
        return dict(cast(dict[str, object] | None, self._hparams_map().get(resolved_sampler)) or {})

    @staticmethod
    def _collate_refresh(batch: list[tuple[BatchInput, torch.Tensor, str]]) -> RefreshBatch:
        return {
            "input_ids": torch.stack([x[0]["input_ids"] for x in batch], dim=0),
            "attention_mask": torch.stack([x[0]["attention_mask"] for x in batch], dim=0),
        }

    def iter_refresh_batches(self) -> list[RefreshBatch]:
        """Return deterministic tokenized batches for sampler refresh embedding updates."""
        loader = self._build_dataloader(
            "train",
            shuffle=False,
            collate_fn=self._collate_refresh,
        )
        return list(loader)

    def set_gcbs_indices(self, indices: Sequence[int]) -> None:
        """Update GCBS sampler indices for the next epoch."""
        if self.train_sampler is None:
            raise RuntimeError("GCBS sampler is not initialized.")
        self.train_sampler.set_indices(indices)

    def set_dpp_embeddings(self, embeddings: torch.Tensor) -> None:
        """Update DPP sampler embeddings for diversity sampling."""
        if self.train_batch_sampler is None:
            raise RuntimeError("DPP batch sampler is not initialized.")
        self.train_batch_sampler.set_embeddings(embeddings)

    def train_dataloader(self) -> DataLoader:
        """Build and return the training dataloader."""
        sampler_type = self.get_sampler_type()
        if sampler_type == "gcbs" and self.train_sampler is None:
            raise RuntimeError("GCBS sampler is not initialized. Call setup() first.")
        if sampler_type == "dpp" and self.train_batch_sampler is None:
            raise RuntimeError("DPP batch sampler is not initialized. Call setup() first.")
        if sampler_type == "dpp":
            return self._build_dataloader(
                "train",
                batch_sampler=self.train_batch_sampler,
                collate_fn=self._collate,
            )
        return self._build_dataloader(
            "train",
            drop_last=bool(self._hparams_map().get("drop_last", False)),
            shuffle=sampler_type not in {"gcbs", "dpp"},
            sampler=self.train_sampler if sampler_type == "gcbs" else None,
            collate_fn=self._collate,
        )

    def val_dataloader(self) -> DataLoader:
        """Build and return the validation dataloader."""
        return self._build_dataloader(
            "val",
            collate_fn=self._collate,
        )

    def test_dataloader(self) -> DataLoader:
        """Build and return the test dataloader."""
        return self._build_dataloader(
            "test",
            collate_fn=self._collate,
        )

if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parents[2]
    data_root = root_dir / "tmp"
    dataset_name = "contrastive_datamodule_self_test"
    dataset_dir = data_root / dataset_name
    cache_dir = data_root / "hf_cache"
    if dataset_dir.exists():
        shutil.rmtree(dataset_dir)
    dataset_dir.mkdir(parents=True, exist_ok=True)

    def _write_split(name: str, rows: list[str]) -> None:
        (dataset_dir / name).write_text(
            "text,label_a,label_b\n" + "".join(rows),
            encoding="utf-8",
        )

    try:
        _write_split("train.csv", ["sample1,1,0\n", "sample2,0,1\n", "sample3,1,1\n", "sample4,0,0\n"])
        _write_split("dev.csv", ["dev1,1,0\n", "dev2,0,1\n"])
        _write_split("test.csv", ["test1,1,1\n", "test2,0,0\n"])

        shuffle_dm = ContrastiveDataModule(
            data_dir=str(data_root),
            dataset_name=dataset_name,
            batch_size=2,
            sampler_type="shuffle",
            num_workers=0,
            pin_memory=False,
            tokenizer_name="roberta-base",
            hf_cache_dir=str(cache_dir),
            hf_num_proc=1,
        )
        shuffle_dm.prepare_data()
        shuffle_dm.setup()
        shuffle_batch = next(iter(shuffle_dm.train_dataloader()))
        assert shuffle_batch[0]["input_ids"].shape[0] == 2
        assert shuffle_batch[1].shape == (2, 2)

        gcbs_dm = ContrastiveDataModule(
            data_dir=str(data_root),
            dataset_name=dataset_name,
            batch_size=2,
            sampler_type="gcbs",
            num_workers=0,
            pin_memory=False,
            tokenizer_name="roberta-base",
            hf_cache_dir=str(cache_dir),
            hf_num_proc=1,
        )
        gcbs_dm.prepare_data()
        gcbs_dm.setup()
        gcbs_dm.set_gcbs_indices([3, 2, 1, 0])
        gcbs_batch = next(iter(gcbs_dm.train_dataloader()))
        assert gcbs_batch[1].shape == (2, 2)

        dpp_dm = ContrastiveDataModule(
            data_dir=str(data_root),
            dataset_name=dataset_name,
            batch_size=2,
            sampler_type="dpp",
            num_workers=0,
            pin_memory=False,
            seed=0,
            tokenizer_name="roberta-base",
            hf_cache_dir=str(cache_dir),
            hf_num_proc=1,
        )
        dpp_dm.prepare_data()
        dpp_dm.setup()
        try:
            _ = next(iter(dpp_dm.train_dataloader()))
        except RuntimeError:
            pass
        else:
            raise AssertionError("DPP sampler must require embeddings before iteration")

        dpp_dm.set_dpp_embeddings(torch.eye(4, dtype=torch.float32))
        dpp_batch = next(iter(dpp_dm.train_dataloader()))
        assert dpp_batch[1].shape == (2, 2)

    finally:
        shutil.rmtree(dataset_dir, ignore_errors=True)

    print("ContrastiveDataModule self-test passed.")
