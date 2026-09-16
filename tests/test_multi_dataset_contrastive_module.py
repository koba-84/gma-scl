import pytest
import torch
from omegaconf import OmegaConf

from src.models.loss.multi_dataset_mxclr import MultiDatasetMXCLR
from src.models.multi_dataset_contrastive_module import MultiDatasetContrastiveLitModule


class _FeatureEncoder(torch.nn.Module):
    hidden_size = 4

    def forward(self, inputs: dict[str, torch.Tensor]) -> torch.Tensor:
        return inputs["input_ids"].float()


def test_multi_dataset_contrastive_module_processes_mixed_batch() -> None:
    loss = MultiDatasetMXCLR(torch.eye(3), instance_temperature=0.2, graph_temperature=0.3)
    module = MultiDatasetContrastiveLitModule(
        encoder=_FeatureEncoder(),
        projection_head=torch.nn.Identity(),
        optimizer=torch.optim.Adam,
        scheduler=None,
        loss_fn=loss,
    )
    inputs = {
        "input_ids": torch.randn(3, 4),
        "attention_mask": torch.ones(3, 4),
        "dataset_id": torch.tensor([0, 1, 0]),
    }
    labels = torch.eye(3)

    value = module.model_step((inputs, labels))

    assert value.ndim == 0
    assert torch.isfinite(value)


def test_multi_dataset_contrastive_module_rejects_forbidden_loss() -> None:
    with pytest.raises(TypeError, match="requires MultiDatasetMXCLR"):
        MultiDatasetContrastiveLitModule(
            encoder=_FeatureEncoder(),
            projection_head=torch.nn.Identity(),
            optimizer=torch.optim.Adam,
            scheduler=None,
            loss_fn=torch.nn.MSELoss(),
        )


def test_multi_dataset_hydra_config_resolves_mixed_stages(compose_train_config) -> None:
    cfg = compose_train_config(
        [
            "data=multi_dataset",
            "contrastive/model=multi_dataset",
            "classification/strategy@classification.model=multi_dataset",
        ]
    )

    assert (
        cfg.contrastive.model.loss_fn._target_
        == "src.models.loss.multi_dataset_mxclr.MultiDatasetMXCLR"
    )
    assert cfg.contrastive.data.dataset_names == ["aapd", "reuters21578", "uklex"]
    assert cfg.contrastive.data.dataset_num_classes == {
        "aapd": 54,
        "reuters21578": 90,
        "uklex": 69,
    }
    assert "warmup_ratio" not in cfg.contrastive.model
    assert "warmup_start_factor" not in cfg.contrastive.model
    resolved_model = OmegaConf.to_yaml(cfg.contrastive.model)
    for forbidden in ("idf", "npmi", "ranking", "listmle", "zlpr"):
        assert forbidden not in resolved_model.lower()
    assert cfg.classification.model.dataset_names == ["aapd", "reuters21578", "uklex"]
    assert cfg.classification.model.label_offsets == {
        "aapd": 0,
        "reuters21578": 54,
        "uklex": 144,
    }
    assert cfg.classification.model.classifier_lr_by_dataset == {
        "aapd": 5.0e-4,
        "reuters21578": 5.0e-4,
        "uklex": 5.0e-4,
    }
    assert cfg.classification.model.encoder_freeze is True


def test_multi_dataset_cdt_hydra_config_resolves_covariance_profile(compose_train_config) -> None:
    cfg = compose_train_config(
        [
            "data=multi_dataset",
            "contrastive/model=multi_dataset_cdt",
            "classification/strategy@classification.model=multi_dataset",
        ]
    )

    assert (
        cfg.contrastive.model._target_
        == "src.models.multi_dataset_cdt_module.MultiDatasetCDTLitModule"
    )
    assert (
        cfg.contrastive.model.loss_fn._target_
        == "src.models.loss.multi_dataset_cdt.MultiDatasetCDT"
    )
    assert cfg.contrastive.model.loss_fn.embedding_dim == 128
    assert cfg.contrastive.model.loss_fn.instance_temperature == 0.1
    assert cfg.contrastive.model.loss_fn.graph_temperature == 0.01
    assert "critic_optimizer" not in cfg.contrastive.model
    assert cfg.classification.model._target_ == (
        "src.models.multi_dataset_finetune_module.MultiDatasetFinetuneLitModule"
    )
