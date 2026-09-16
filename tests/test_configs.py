from __future__ import annotations

import hydra
import pytest
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig, open_dict


def test_train_config(cfg_train: DictConfig) -> None:
    HydraConfig().set_config(cfg_train)

    assert cfg_train
    assert cfg_train.contrastive
    assert cfg_train.classification
    assert cfg_train.trainer
    assert "work_dir" not in cfg_train.paths
    assert "log_dir" not in cfg_train.paths

    hydra.utils.instantiate(cfg_train.contrastive.data)
    hydra.utils.instantiate(cfg_train.contrastive.model)
    hydra.utils.instantiate(cfg_train.contrastive.trainer)
    hydra.utils.instantiate(cfg_train.classification.data)
    hydra.utils.instantiate(cfg_train.classification.model)
    hydra.utils.instantiate(cfg_train.classification.trainer)
    assert cfg_train.trainer.deterministic is True
    assert cfg_train.contrastive.trainer.deterministic is True
    assert cfg_train.classification.trainer.deterministic is True
    assert cfg_train.callbacks.model_checkpoint.monitor == "classification/val/f1_macro"


@pytest.mark.parametrize(
    ("target", "params"),
    [
        pytest.param("torch.nn.BCEWithLogitsLoss", {}, id="bce_with_logits"),
        pytest.param(
            "src.models.loss.classification.AsymmetricLoss",
            {"gamma_pos": 0.0, "gamma_neg": 1.0, "margin": 0.0},
            id="asymmetric_loss",
        ),
        pytest.param("src.models.loss.classification.ZLPRLoss", {}, id="zlpr_loss"),
    ],
)
def test_classification_loss_variants_config(
    cfg_train: DictConfig,
    target: str,
    params: dict[str, float],
) -> None:
    HydraConfig().set_config(cfg_train)

    cfg = cfg_train.copy()
    with open_dict(cfg):
        cfg.classification.model.criterion._target_ = target
        for key, value in params.items():
            cfg.classification.model.criterion[key] = value

    hydra.utils.instantiate(cfg.classification.model)
