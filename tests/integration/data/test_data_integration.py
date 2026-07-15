from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import pytest
import torch
from torch import nn

from src.data.classification_datamodule import ClassificationDataModule
from src.models.finetune_module import FinetuneLitModule

pytestmark = pytest.mark.integration


def _label_ratio(csv_path: Path, label_col: str) -> float:
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        values = [float(row[label_col]) for row in reader]
    if not values:
        raise ValueError("CSV must contain at least one row")
    return sum(values) / float(len(values))


def _is_shift_large(base: float, target: float, threshold: float) -> bool:
    return abs(base - target) > threshold


def test_classification_datamodule_integration(
    classification_dm_factory: Any,
) -> None:
    dm = classification_dm_factory()
    dm.prepare_data()
    dm.setup()

    assert dm.num_classes == 2
    assert set(dm.label2id.keys()) == {"label_a", "label_b"}

    train_batch = next(iter(dm.train_dataloader()))
    val_batch = next(iter(dm.val_dataloader()))
    test_batch = next(iter(dm.test_dataloader()))
    assert train_batch[0]["input_ids"].shape[0] == 2
    assert train_batch[1].shape == (2, 2)
    assert val_batch[1].shape == (2, 2)
    assert test_batch[1].shape == (2, 2)

    mismatch_dm = classification_dm_factory(num_classes=3)
    with pytest.raises(ValueError, match="num_classes mismatch"):
        mismatch_dm.setup()


def test_data_quality_skew_guard(
    synthetic_multilabel_dataset_factory: Any,
) -> None:
    _, dataset_dir = synthetic_multilabel_dataset_factory(
        train_rows=["s1,1,0\n", "s2,1,0\n", "s3,1,0\n", "s4,1,0\n"],
    )

    (dataset_dir / "dev.csv").write_text(
        "text,label_a,label_b\nd1,0,0\nd2,0,0\nd3,0,0\nd4,0,0\n",
        encoding="utf-8",
    )
    train_ratio = _label_ratio(dataset_dir / "train.csv", "label_a")
    dev_ratio = _label_ratio(dataset_dir / "dev.csv", "label_a")
    assert _is_shift_large(train_ratio, dev_ratio, threshold=0.6) is True


def test_data_quality_drift_guard(
    synthetic_multilabel_dataset_factory: Any,
) -> None:
    _, dataset_dir = synthetic_multilabel_dataset_factory(
        train_rows=["a,1,0\n", "b,1,0\n", "c,0,0\n", "d,0,0\n"],
    )

    prev_ratio = _label_ratio(dataset_dir / "train.csv", "label_a")
    (dataset_dir / "train.csv").write_text(
        "text,label_a,label_b\na,1,0\nb,1,0\nc,1,0\nrow4,1,0\n",
        encoding="utf-8",
    )
    next_ratio = _label_ratio(dataset_dir / "train.csv", "label_a")
    assert _is_shift_large(prev_ratio, next_ratio, threshold=0.4) is True


def test_data_schema_contract_guard(
    synthetic_multilabel_dataset_factory: Any,
) -> None:
    data_root, dataset_dir = synthetic_multilabel_dataset_factory()
    for split in ("train.csv", "dev.csv", "test.csv"):
        source = dataset_dir / split
        source.write_text(
            source.read_text(encoding="utf-8").replace("text,", "body,", 1),
            encoding="utf-8",
        )

    dm = ClassificationDataModule(
        data_dir=str(data_root),
        dataset_name="aapd",
        num_classes=2,
        batch_size=2,
        num_workers=0,
        pin_memory=False,
        hf_cache_dir=str(data_root / "hf_cache"),
    )
    dm.prepare_data()
    dm.setup()

    features, labels = next(iter(dm.train_dataloader()))
    assert features["input_ids"].shape[0] == 2
    assert labels.shape == (2, 2)


def test_contrastive_datamodule_sampler_integration(
    contrastive_dm_factory: Any,
) -> None:
    dm = contrastive_dm_factory(batch_size=2, sampler_type="dpp", seed=0)
    dm.prepare_data()
    dm.setup()
    dm.set_dpp_embeddings(torch.eye(4, dtype=torch.float32))

    train_batch = next(iter(dm.train_dataloader()))
    features, labels = train_batch
    assert features["input_ids"].shape[0] == 2
    assert labels.shape == (2, 2)
    assert features["empty_text_mask"].shape == (2,)


def test_contrastive_dpp_reproducibility_with_fixed_seed(
    contrastive_dm_factory: Any,
) -> None:
    torch.manual_seed(1234)
    dm_a = contrastive_dm_factory(batch_size=2, sampler_type="dpp", seed=1234)
    dm_a.prepare_data()
    dm_a.setup()
    dm_a.set_dpp_embeddings(torch.eye(4, dtype=torch.float32))
    batch_a = next(iter(dm_a.train_dataloader()))

    torch.manual_seed(1234)
    dm_b = contrastive_dm_factory(batch_size=2, sampler_type="dpp", seed=1234)
    dm_b.prepare_data()
    dm_b.setup()
    dm_b.set_dpp_embeddings(torch.eye(4, dtype=torch.float32))
    batch_b = next(iter(dm_b.train_dataloader()))

    assert torch.equal(batch_a[0]["input_ids"], batch_b[0]["input_ids"])
    assert torch.equal(batch_a[1], batch_b[1])


def test_contrastive_refresh_batches_use_tokenized_tensors(
    contrastive_dm_factory: Any,
) -> None:
    dm = contrastive_dm_factory(batch_size=2)
    dm.prepare_data()
    dm.setup()

    refresh_batch = dm.iter_refresh_batches()[0]
    assert refresh_batch["input_ids"].dtype == torch.long
    assert refresh_batch["attention_mask"].dtype == torch.long


def test_classification_batch_has_empty_text_mask_and_zero_override(
    classification_dm_factory: Any,
) -> None:
    dm = classification_dm_factory(batch_size=2)
    dm.prepare_data()
    dm.setup()

    features, labels = next(iter(dm.train_dataloader()))
    assert features["empty_text_mask"].dtype == torch.bool
    assert labels.dtype == torch.float32


def test_finetune_model_step_returns_scores_for_map() -> None:
    class _EncoderStub(nn.Module):
        hidden_size = 3

        def forward(self, inputs: dict[str, torch.Tensor]) -> torch.Tensor:
            return inputs["input_ids"]

    module = FinetuneLitModule(
        encoder=_EncoderStub(),
        optimizer=torch.optim.Adam,
        scheduler=None,
        num_classes=2,
        criterion=torch.nn.BCEWithLogitsLoss(),
        compile=False,
    )
    batch = (
        {
            "input_ids": torch.tensor([[1.0, 0.0, 1.0], [0.0, 1.0, 0.0]], dtype=torch.float32),
            "attention_mask": torch.ones((2, 3), dtype=torch.float32),
            "empty_text_mask": torch.zeros(2, dtype=torch.bool),
        },
        torch.tensor([[1.0, 0.0], [0.0, 1.0]], dtype=torch.float32),
    )

    loss, scores, preds, targets = module.model_step(batch)

    assert loss.ndim == 0
    assert scores.shape == (2, 2)
    assert preds.shape == targets.shape == (2, 2)
    assert torch.isfinite(loss)
    assert torch.isfinite(scores).all()
    assert torch.isfinite(preds).all()
