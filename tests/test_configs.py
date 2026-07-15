import inspect

import hydra
import pytest
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig, open_dict


def test_train_config(cfg_train: DictConfig) -> None:
    """Tests the training configuration provided by the `cfg_train` pytest fixture.

    :param cfg_train: A DictConfig containing a valid training configuration.
    """
    assert cfg_train
    assert cfg_train.contrastive
    assert cfg_train.classification
    assert cfg_train.trainer

    HydraConfig().set_config(cfg_train)

    hydra.utils.instantiate(cfg_train.contrastive.data)
    hydra.utils.instantiate(cfg_train.contrastive.model)
    hydra.utils.instantiate(cfg_train.contrastive.trainer)
    hydra.utils.instantiate(cfg_train.classification.data)
    hydra.utils.instantiate(cfg_train.classification.model)
    hydra.utils.instantiate(cfg_train.classification.trainer)
    assert cfg_train.trainer.deterministic is True
    assert cfg_train.contrastive.trainer.deterministic is True
    assert cfg_train.classification.trainer.deterministic is True


def test_classification_stage_config(cfg_train: DictConfig) -> None:
    """Tests classification stage config from train.yaml.

    :param cfg_train: A DictConfig containing a valid training configuration.
    """
    assert cfg_train.classification
    assert cfg_train.classification.data
    assert cfg_train.classification.model
    assert cfg_train.classification.trainer

    HydraConfig().set_config(cfg_train)

    hydra.utils.instantiate(cfg_train.classification.data)
    hydra.utils.instantiate(cfg_train.classification.model)
    hydra.utils.instantiate(cfg_train.classification.trainer)
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
    """Tests classification model instantiation with supported loss variants."""
    HydraConfig().set_config(cfg_train)

    cfg = cfg_train.copy()
    with open_dict(cfg):
        cfg.classification.model.criterion._target_ = target
        for key, value in params.items():
            cfg.classification.model.criterion[key] = value
    hydra.utils.instantiate(cfg.classification.model)


@pytest.mark.parametrize(
    ("overrides", "assert_data_dir_suffix"),
    [
        pytest.param(["contrastive/model=mxclr"], True, id="mxclr_default"),
        pytest.param(["contrastive/model=mxclr_rank"], True, id="mxclr_rank_default"),
        pytest.param(
            [
                "contrastive/model=mxclr",
                "contrastive/model/agg@contrastive.model.loss_fn=BERTScore_F1",
            ],
            False,
            id="mxclr_bertscore_f1",
        ),
        pytest.param(
            [
                "contrastive/model=mxclr",
                "contrastive/model/agg@contrastive.model.loss_fn=BERTScore_F1_Uniform",
            ],
            False,
            id="mxclr_bertscore_f1_uniform",
        ),
        pytest.param(
            [
                "contrastive/model=mxclr",
                "contrastive/model/agg@contrastive.model.loss_fn=BERTScore_Precision",
            ],
            False,
            id="mxclr_bertscore_precision",
        ),
        pytest.param(
            [
                "contrastive/model=mxclr",
                "contrastive/model/agg@contrastive.model.loss_fn=BERTScore_Recall",
            ],
            False,
            id="mxclr_bertscore_recall",
        ),
        pytest.param(
            [
                "contrastive/model=mxclr_rank",
                "contrastive/model/agg@contrastive.model.loss_fn=BERTScore_F1_Uniform",
            ],
            False,
            id="mxclr_rank_bertscore_f1_uniform",
        ),
        pytest.param(
            [
                "contrastive/model=mxclr_rank",
                "contrastive/model/agg@contrastive.model.loss_fn=BERTScore_F1",
            ],
            False,
            id="mxclr_rank_bertscore_f1",
        ),
    ],
)
def test_mxclr_family_configs_instantiate_without_manual_label_stats(
    compose_train_config,
    stub_mxclr_dependencies: None,
    overrides: list[str],
    assert_data_dir_suffix: bool,
) -> None:
    cfg = compose_train_config(overrides)

    if assert_data_dir_suffix:
        assert cfg.contrastive.model.loss_fn.data_dir.endswith("/data/")
    hydra.utils.instantiate(cfg.contrastive.model)


def test_mxclr_default_sbert_model_name(compose_train_config) -> None:
    cfg = compose_train_config(["contrastive/model=mxclr"])

    assert (
        cfg.contrastive.model.loss_fn.agg._target_
        == "src.models.loss.agg.bertscore_f1.BERTScoreF1Graph"
    )
    assert (
        cfg.contrastive.model.loss_fn.sbert_model_name
        == "sentence-transformers/all-roberta-large-v1"
    )
    assert cfg.contrastive.model.loss_fn.sbert_max_length == 512
    assert cfg.contrastive.model.loss_fn.whitening is False
    assert cfg.contrastive.data.max_length == 512
    assert cfg.classification.data.max_length == 512
    assert "gamma" not in cfg.contrastive.model.loss_fn


@pytest.mark.parametrize(
    ("overrides", "expected_keys"),
    [
        pytest.param(["contrastive/model=base"], {"temperature", "eps"}, id="base"),
        pytest.param(["contrastive/model=ml_supcon"], {"temperature", "eps"}, id="ml_supcon"),
        pytest.param(
            ["contrastive/model=msc"],
            {"alpha", "beta", "temperature"},
            id="msc",
        ),
        pytest.param(
            ["contrastive/model=mxclr"],
            {
                "data_dir",
                "instance_temperature",
                "graph_temperature",
                "dataset_name",
                "sbert_model_name",
                "sbert_max_length",
                "whitening",
                "agg",
            },
            id="mxclr",
        ),
        pytest.param(
            ["contrastive/model=mxclr_rank"],
            {
                "data_dir",
                "instance_temperature",
                "graph_temperature",
                "rank_temperature",
                "lambda_rank",
                "dataset_name",
                "sbert_model_name",
                "sbert_max_length",
                "whitening",
                "agg",
            },
            id="mxclr_rank",
        ),
    ],
)
def test_contrastive_loss_configs_declare_all_runtime_init_args(
    compose_train_config,
    overrides: list[str],
    expected_keys: set[str],
) -> None:
    cfg = compose_train_config(overrides)
    loss_cfg = cfg.contrastive.model.loss_fn

    target = hydra.utils.get_class(loss_cfg._target_)
    signature = inspect.signature(target)
    runtime_keys = {
        name
        for name, parameter in signature.parameters.items()
        if name != "self"
        and parameter.kind
        in {
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        }
    }

    assert runtime_keys == expected_keys
    assert runtime_keys.issubset(set(loss_cfg.keys()))
    legacy_temperature_keys = {"temp", "tau", "tau_s", "temp_attract", "temp_repulse"}
    assert legacy_temperature_keys.isdisjoint(set(loss_cfg.keys()))


@pytest.mark.parametrize(
    "classification_data_override",
    [
        "classification/data=aapd",
        "classification/data=rcv1",
        "classification/data=rcv1_3k",
    ],
)
def test_classification_data_max_length_defaults_to_512(
    compose_train_config,
    classification_data_override: str,
) -> None:
    cfg = compose_train_config([classification_data_override])

    assert cfg.classification.data.max_length == 512
