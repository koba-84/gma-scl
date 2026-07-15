from __future__ import annotations

import os
from pathlib import Path
from typing import Any, cast

import pytest
import torch
from omegaconf import DictConfig, OmegaConf, open_dict

from src.train import train

pytestmark = [pytest.mark.integration, pytest.mark.slow]


def test_train_epoch_double_val_loop(configured_train_cfg) -> None:
    cfg_train = configured_train_cfg(
        {
            "trainer.max_epochs": 1,
            "trainer.val_check_interval": 0.5,
        }
    )
    train(cfg_train)


def test_train_ddp_sim(configured_train_cfg) -> None:
    cfg_train = configured_train_cfg(
        {
            "trainer.accelerator": "cpu",
            "trainer.devices": 2,
            "trainer.strategy": "ddp_find_unused_parameters_true",
        }
    )

    contrastive_trainer = cast(
        dict[str, Any], OmegaConf.to_container(cfg_train.contrastive.trainer, resolve=True)
    )
    classification_trainer = cast(
        dict[str, Any], OmegaConf.to_container(cfg_train.classification.trainer, resolve=True)
    )

    assert contrastive_trainer["accelerator"] == "cpu"
    assert int(contrastive_trainer["devices"]) == 2
    assert contrastive_trainer["strategy"] == "ddp_find_unused_parameters_true"
    assert classification_trainer["accelerator"] == "cpu"
    assert int(classification_trainer["devices"]) == 2
    assert classification_trainer["strategy"] == "ddp_find_unused_parameters_true"


def test_train_resume(tmp_path: Path, cfg_train: DictConfig) -> None:
    with open_dict(cfg_train):
        cfg_train.contrastive.model = None
        cfg_train.classification.test = False
        cfg_train.classification.trainer.max_epochs = 1

    train(cfg_train)

    files = os.listdir(tmp_path / "checkpoints")
    assert "last.ckpt" in files
    assert "epoch_000.ckpt" in files
    before_resume = torch.load(tmp_path / "checkpoints" / "last.ckpt", map_location="cpu")
    before_epoch = int(before_resume["epoch"])

    with open_dict(cfg_train):
        cfg_train.classification.ckpt_path = str(tmp_path / "checkpoints" / "last.ckpt")
        cfg_train.classification.trainer.max_epochs = 2

    train(cfg_train)

    last_ckpt_path = tmp_path / "checkpoints" / "last.ckpt"
    assert last_ckpt_path.exists()
    ckpt_state = torch.load(last_ckpt_path, map_location="cpu")
    assert int(ckpt_state["epoch"]) > before_epoch
