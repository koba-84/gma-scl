from __future__ import annotations

import pytest

from src.train import train
from tests.support.run_if import run_if

pytestmark = [pytest.mark.integration, pytest.mark.gpu]


@run_if(min_gpus=1)
def test_train_fast_dev_run_gpu(configured_train_cfg) -> None:
    cfg_train = configured_train_cfg(
        {
            "trainer.fast_dev_run": True,
            "trainer.accelerator": "gpu",
        }
    )
    train(cfg_train)
