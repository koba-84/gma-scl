from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path
from typing import Any, cast

import pytest
import rootutils
from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig, open_dict

from tests.support.fixtures.datasets import write_synthetic_multilabel_dataset


def _set_cfg_value(cfg: DictConfig, path: str, value: object) -> None:
    parts = path.split(".")
    target = cfg
    for part in parts[:-1]:
        target = cast(Any, target)[part]
    cast(Any, target)[parts[-1]] = value


@pytest.fixture(scope="package")
def cfg_train_global() -> DictConfig:
    with initialize(version_base="1.3", config_path="../../../configs"):
        cfg = compose(config_name="train.yaml", return_hydra_config=True, overrides=[])

        with open_dict(cfg):
            root_dir = str(rootutils.find_root(indicator=".project-root"))
            os.environ["PROJECT_ROOT"] = root_dir
            cfg.paths.root_dir = root_dir
            cfg.trainer.max_epochs = 1
            cfg.trainer.limit_train_batches = 0.01
            cfg.trainer.limit_val_batches = 0.1
            cfg.trainer.limit_test_batches = 0.1
            cfg.trainer.accelerator = "cpu"
            cfg.trainer.devices = 1
            cfg.contrastive.trainer.max_epochs = 1
            cfg.contrastive.trainer.limit_train_batches = 2
            cfg.contrastive.trainer.limit_val_batches = 1
            cfg.classification.trainer.max_epochs = 1
            cfg.classification.trainer.limit_train_batches = 2
            cfg.classification.trainer.limit_val_batches = 1
            cfg.classification.trainer.limit_test_batches = 1
            cfg.contrastive.data.num_workers = 0
            cfg.contrastive.data.pin_memory = False
            cfg.classification.data.num_workers = 0
            cfg.classification.data.pin_memory = False
            cfg.classification.model.encoder_freeze = False
            cfg.extras.print_config = False
            cfg.extras.enforce_tags = False
            cfg.logger = None

    return cfg


@pytest.fixture(scope="function")
def cfg_train(cfg_train_global: DictConfig, tmp_path: Path) -> Generator[DictConfig, None, None]:
    cfg = cfg_train_global.copy()
    synthetic_data_root = tmp_path / "data"
    synthetic_dataset_name = "aapd"
    write_synthetic_multilabel_dataset(
        data_root=synthetic_data_root,
        dataset_name=synthetic_dataset_name,
    )

    with open_dict(cfg):
        cfg.paths.output_dir = str(tmp_path)
        cfg.paths.log_dir = str(tmp_path)
        cfg.paths.data_dir = str(synthetic_data_root)
        cfg.contrastive.data.data_dir = str(synthetic_data_root)
        cfg.contrastive.data.dataset_name = synthetic_dataset_name
        cfg.contrastive.data.hf_cache_dir = str(tmp_path / "hf_cache")
        cfg.classification.data.data_dir = str(synthetic_data_root)
        cfg.classification.data.dataset_name = synthetic_dataset_name
        cfg.classification.data.num_classes = 2
        cfg.classification.data.hf_cache_dir = str(tmp_path / "hf_cache")

    yield cfg

    GlobalHydra.instance().clear()


@pytest.fixture(scope="function")
def configured_train_cfg(cfg_train: DictConfig):
    HydraConfig().set_config(cfg_train)

    def _configure(updates: dict[str, object] | None = None) -> DictConfig:
        if updates:
            with open_dict(cfg_train):
                for path, value in updates.items():
                    _set_cfg_value(cfg_train, path, value)
        return cfg_train

    return _configure


@pytest.fixture(scope="function")
def compose_train_config(monkeypatch: pytest.MonkeyPatch):
    root_dir = str(rootutils.find_root(indicator=".project-root"))
    monkeypatch.setenv("PROJECT_ROOT", root_dir)

    def _compose(overrides: list[str] | None = None) -> DictConfig:
        GlobalHydra.instance().clear()
        with initialize(version_base="1.3", config_path="../../../configs"):
            cfg = compose(
                config_name="train.yaml",
                return_hydra_config=True,
                overrides=overrides or [],
            )
        HydraConfig().set_config(cfg)
        return cfg

    return _compose
