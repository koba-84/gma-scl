from __future__ import annotations

from pathlib import Path

import pytest
import torch

from src.train import train

pytestmark = pytest.mark.integration


def test_train_fast_dev_run(configured_train_cfg) -> None:
    cfg_train = configured_train_cfg(
        {
            "trainer.fast_dev_run": True,
            "trainer.accelerator": "cpu",
        }
    )
    train(cfg_train)


def test_train_includes_classification_test(tmp_path: Path, configured_train_cfg) -> None:
    cfg_train = configured_train_cfg(
        {
            "contrastive.trainer.max_epochs": 1,
            "classification.trainer.max_epochs": 1,
            "classification.test": True,
        }
    )
    assert str(tmp_path) == cfg_train.paths.output_dir
    train_metric_dict, _ = train(cfg_train)

    assert (tmp_path / "checkpoints").exists()
    assert "classification/test/f1_micro" in train_metric_dict
    assert "classification/test/map" in train_metric_dict
    f1 = train_metric_dict["classification/test/f1_micro"]
    map_score = train_metric_dict["classification/test/map"]
    f1_tensor = f1 if isinstance(f1, torch.Tensor) else torch.tensor(float(f1))
    map_tensor = (
        map_score if isinstance(map_score, torch.Tensor) else torch.tensor(float(map_score))
    )
    assert torch.isfinite(f1_tensor)
    assert torch.isfinite(map_tensor)
    assert 0.0 <= float(f1_tensor) <= 1.0
    assert 0.0 <= float(map_tensor) <= 1.0


def test_train_sets_pretrained_encoder_path_from_contrastive_stage(configured_train_cfg) -> None:
    cfg_train = configured_train_cfg(
        {
            "contrastive.trainer.fast_dev_run": True,
            "classification.trainer.fast_dev_run": True,
            "trainer.accelerator": "cpu",
            "classification.model.pretrained_encoder_path": None,
            "classification.test": False,
        }
    )

    train(cfg_train)

    pretrained_path = cfg_train.classification.model.pretrained_encoder_path
    assert pretrained_path is not None
    assert str(pretrained_path).endswith("contrastive_last.ckpt")
