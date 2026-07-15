from __future__ import annotations

import pytest
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig, open_dict

from src.train import train
from tests.support.run_if import run_if

pytestmark = [pytest.mark.integration, pytest.mark.slow, pytest.mark.gpu]


@run_if(min_gpus=1)
def test_train_epoch_gpu_amp(cfg_train: DictConfig) -> None:
    HydraConfig().set_config(cfg_train)
    with open_dict(cfg_train):
        cfg_train.trainer.max_epochs = 1
        cfg_train.trainer.accelerator = "gpu"
        cfg_train.trainer.precision = 16
    train(cfg_train)
