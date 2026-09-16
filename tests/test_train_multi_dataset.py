from __future__ import annotations

from lightning import LightningModule
from omegaconf import OmegaConf

from src.train import _stage_callbacks_config


class _DatasetSpecificStateModel(LightningModule):
    uses_dataset_specific_best_state = True


def test_dataset_specific_state_model_disables_global_checkpoint_callbacks() -> None:
    stage_cfg = OmegaConf.create({"callbacks": {"model_checkpoint": {"monitor": "old"}}})
    base_cfg = OmegaConf.create({"callbacks": {"model_checkpoint": {"monitor": "global"}}})

    assert _stage_callbacks_config(stage_cfg, base_cfg, _DatasetSpecificStateModel()) is None


def test_standard_model_keeps_stage_callbacks() -> None:
    stage_cfg = OmegaConf.create({"callbacks": {"model_checkpoint": {"monitor": "stage"}}})
    base_cfg = OmegaConf.create({"callbacks": {"model_checkpoint": {"monitor": "global"}}})

    callbacks = _stage_callbacks_config(stage_cfg, base_cfg, LightningModule())

    assert callbacks.model_checkpoint.monitor == "stage"
