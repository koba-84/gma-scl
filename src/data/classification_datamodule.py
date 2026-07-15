from __future__ import annotations

import shutil
from pathlib import Path
from typing import cast

import rootutils
from torch.utils.data import DataLoader

rootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)

from src.data.tokenized_datamodule_base import TokenizedCSVDataModuleBase


class ClassificationDataModule(TokenizedCSVDataModuleBase):
    """LightningDataModule for tokenized multi-label CSV datasets."""

    def __init__(
        self,
        data_dir: str = "data/",
        dataset_name: str = "20ng",
        num_classes: int | None = None,
        batch_size: int = 64,
        num_workers: int = 0,
        pin_memory: bool = False,
        tokenizer_name: str = "roberta-base",
        max_length: int = 512,
        hf_cache_dir: str = "tmp/hf_cache",
        hf_num_proc: int = 1,
    ) -> None:
        super().__init__(batch_size=batch_size)

        self.save_hyperparameters(logger=False)

    @property
    def num_classes(self) -> int:
        """Execute num_classes and return the resulting value."""
        num_classes = self._hparams_map().get("num_classes")
        if num_classes is not None:
            return int(cast(int | str, num_classes))
        return len(self._label2id)

    def setup(self, stage: str | None = None) -> None:
        """Set up datasets, samplers, and runtime state for the stage."""
        self._setup_tokenized_data()
        num_classes = self._hparams_map().get("num_classes")
        if num_classes is not None:
            expected = int(cast(int | str, num_classes))
            if len(self._label2id) != expected:
                raise ValueError(
                    f"num_classes mismatch: config={expected}, dataset={len(self._label2id)}"
                )

    def train_dataloader(self) -> DataLoader:
        """Build and return the training dataloader."""
        return self._build_dataloader(
            "train",
            shuffle=True,
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
    dataset_name = "classification_datamodule_self_test"
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
        _write_split("train.csv", ["sample1,1,0\n", "sample2,0,1\n", "sample3,1,1\n"])
        _write_split("dev.csv", ["dev1,1,0\n", "dev2,0,1\n"])
        _write_split("test.csv", ["test1,1,1\n", "test2,0,0\n"])

        dm = ClassificationDataModule(
            data_dir=str(data_root),
            dataset_name=dataset_name,
            batch_size=2,
            num_workers=0,
            pin_memory=False,
            tokenizer_name="roberta-base",
            hf_cache_dir=str(cache_dir),
            hf_num_proc=1,
        )
        dm.prepare_data()
        dm.setup()
        assert dm.num_classes == 2
        assert set(dm.label2id.keys()) == {"label_a", "label_b"}

        train_batch = next(iter(dm.train_dataloader()))
        assert train_batch[0]["input_ids"].shape[0] == 2
        assert train_batch[1].shape == (2, 2)

        mismatch_dm = ClassificationDataModule(
            data_dir=str(data_root),
            dataset_name=dataset_name,
            num_classes=3,
            batch_size=2,
            num_workers=0,
            pin_memory=False,
            tokenizer_name="roberta-base",
            hf_cache_dir=str(cache_dir),
            hf_num_proc=1,
        )
        try:
            mismatch_dm.setup()
        except ValueError as exc:
            assert "num_classes mismatch" in str(exc)
        else:
            raise AssertionError("num_classes mismatch must raise ValueError")
    finally:
        shutil.rmtree(dataset_dir, ignore_errors=True)

    print("ClassificationDataModule self-test passed.")
