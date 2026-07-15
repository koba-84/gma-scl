from __future__ import annotations

from typing import Any

import pytest
from omegaconf import OmegaConf

from src.utils.logging_utils import log_hyperparameters


def _build_cfg(payload: dict[str, Any]) -> Any:
    return OmegaConf.create(payload)


def test_log_hyperparameters_resolves_interpolations(
    capture_logger,
    logging_runtime,
) -> None:
    trainer, model = logging_runtime
    cfg = _build_cfg(
        {
            "trainer": {"accelerator": "gpu", "devices": 1},
            "contrastive": {
                "model": {
                    "loss_fn": {
                        "_target_": "src.models.loss.mxclr.MXCLR",
                    }
                },
                "trainer": {
                    "accelerator": "${trainer.accelerator}",
                    "devices": "${trainer.devices}",
                },
            },
            "classification": {
                "model": {
                    "criterion": {
                        "_target_": "torch.nn.BCEWithLogitsLoss",
                    }
                },
                "trainer": {
                    "accelerator": "${trainer.accelerator}",
                    "devices": "${trainer.devices}",
                },
            },
            "data": {"dataset_name": "aapd"},
            "callbacks": {},
            "extras": {},
            "task_name": "train",
            "tags": ["dev"],
            "seed": 0,
        }
    )

    log_hyperparameters(
        {
            "cfg": cfg,
            "stage_name": "contrastive",
            "model": model,
            "trainer": trainer,
        }
    )

    assert capture_logger.logged is not None
    assert capture_logger.logged["contrastive"]["trainer"]["accelerator"] == "gpu"
    assert capture_logger.logged["contrastive"]["trainer"]["devices"] == 1
    assert capture_logger.logged["classification"]["trainer"]["accelerator"] == "gpu"
    assert capture_logger.logged["contrastive"]["model"]["loss_name"] == "mxclr"
    assert capture_logger.logged["classification"]["model"]["loss_name"] == "bce"
    assert all("." not in key for key in capture_logger.logged)
    assert "${" not in str(capture_logger.logged["contrastive"])
    assert "${" not in str(capture_logger.logged["classification"])


def test_log_hyperparameters_prefers_stage_runtime_config(
    capture_logger,
    logging_runtime,
) -> None:
    trainer, model = logging_runtime
    cfg = _build_cfg(
        {
            "trainer": {"accelerator": "gpu", "devices": 1},
            "contrastive": {"trainer": {"max_epochs": 80}},
            "classification": {
                "trainer": {
                    "max_epochs": 40,
                    "accelerator": "${trainer.accelerator}",
                },
                "model": {"pretrained_encoder_path": None},
            },
            "callbacks": {},
            "extras": {},
            "task_name": "train",
            "tags": ["dev"],
            "seed": 0,
        }
    )
    stage_cfg = _build_cfg(
        {
            "trainer": {
                "max_epochs": 12,
                "accelerator": "cpu",
            },
            "model": {
                "pretrained_encoder_path": "tmp/contrastive_last.ckpt",
            },
        }
    )

    log_hyperparameters(
        {
            "cfg": cfg,
            "stage_name": "classification",
            "stage_cfg": stage_cfg,
            "model": model,
            "trainer": trainer,
        }
    )

    assert capture_logger.logged is not None
    assert capture_logger.logged["classification"]["trainer"]["max_epochs"] == 12
    assert capture_logger.logged["classification"]["trainer"]["accelerator"] == "cpu"
    assert (
        capture_logger.logged["classification"]["model"]["pretrained_encoder_path"]
        == "tmp/contrastive_last.ckpt"
    )


def test_log_hyperparameters_resolves_stage_runtime_interpolations_with_root_context(
    capture_logger,
    logging_runtime,
) -> None:
    trainer, model = logging_runtime
    cfg = _build_cfg(
        {
            "paths": {
                "root_dir": "/workdir/project",
                "data_dir": "${paths.root_dir}/data",
            },
            "trainer": {"accelerator": "gpu", "devices": 1},
            "contrastive": {
                "data": {
                    "data_dir": "${paths.data_dir}",
                },
                "trainer": {
                    "accelerator": "${trainer.accelerator}",
                },
            },
            "classification": {"trainer": {"max_epochs": 40}},
            "data": {"dataset_name": "aapd"},
            "callbacks": {},
            "extras": {},
            "task_name": "train",
            "tags": ["dev"],
            "seed": 0,
        }
    )
    stage_cfg = _build_cfg(
        {
            "data": {
                "data_dir": "${paths.data_dir}",
                "hf_cache_dir": "${paths.data_dir}/.hf_cache",
            },
            "trainer": {
                "accelerator": "${trainer.accelerator}",
            },
        }
    )

    log_hyperparameters(
        {
            "cfg": cfg,
            "stage_name": "contrastive",
            "stage_cfg": stage_cfg,
            "model": model,
            "trainer": trainer,
        }
    )

    assert capture_logger.logged is not None
    assert capture_logger.logged["contrastive"]["data"]["data_dir"] == "/workdir/project/data"
    assert (
        capture_logger.logged["contrastive"]["data"]["hf_cache_dir"]
        == "/workdir/project/data/.hf_cache"
    )
    assert capture_logger.logged["contrastive"]["trainer"]["accelerator"] == "gpu"


def test_log_hyperparameters_logs_derived_contrastive_aliases(
    capture_logger,
    logging_runtime,
) -> None:
    trainer, model = logging_runtime
    cfg = _build_cfg(
        {
            "contrastive": {
                "model": {
                    "loss_fn": {
                        "_target_": "src.models.loss.mxclr_proto.MXCLRProto",
                        "agg": {
                            "_target_": "src.models.loss.agg.bertscore_f1.BERTScoreF1Graph",
                            "transport_lambda": 0.5,
                        },
                        "graph_temperature_schedule": {
                            "start": 0.5,
                            "end": 0.1,
                        },
                    }
                }
            },
            "classification": {"trainer": {"max_epochs": 40}},
            "data": {"dataset_name": "aapd"},
            "callbacks": {},
            "extras": {},
            "task_name": "train",
            "tags": ["dev"],
            "seed": 0,
        }
    )

    log_hyperparameters(
        {
            "cfg": cfg,
            "stage_name": "contrastive",
            "model": model,
            "trainer": trainer,
        }
    )

    assert capture_logger.logged is not None
    assert capture_logger.logged["contrastive"]["model"]["loss_name"] == "mxclr_proto"
    assert (
        capture_logger.logged["contrastive"]["model"]["loss_fn"]["agg"]["transport_lambda"] == 0.5
    )
    assert capture_logger.logged["contrastive"]["model"]["loss_fn"]["agg_name"] == "BERTScore_F1"
    assert capture_logger.logged["contrastive"]["model"]["loss_fn"]["graph_temperature"] == 0.5


def test_log_hyperparameters_logs_canonical_bertscore_f1_alias(
    capture_logger,
    logging_runtime,
) -> None:
    trainer, model = logging_runtime
    cfg = _build_cfg(
        {
            "contrastive": {
                "model": {
                    "loss_fn": {
                        "_target_": "src.models.loss.mxclr.MXCLR",
                        "agg": {
                            "_target_": "src.models.loss.agg.bertscore_f1.BERTScoreF1Graph",
                            "transport_lambda": 0.5,
                        },
                    }
                }
            },
            "classification": {"trainer": {"max_epochs": 40}},
            "data": {"dataset_name": "aapd"},
            "callbacks": {},
            "extras": {},
            "task_name": "train",
            "tags": ["dev"],
            "seed": 0,
        }
    )

    log_hyperparameters(
        {
            "cfg": cfg,
            "stage_name": "contrastive",
            "model": model,
            "trainer": trainer,
        }
    )

    assert capture_logger.logged is not None
    assert capture_logger.logged["contrastive"]["model"]["loss_fn"]["agg_name"] == "BERTScore_F1"


@pytest.mark.parametrize(
    ("target", "expected"),
    [
        (
            "src.models.loss.agg.bertscore_f1.BERTScorePrecisionGraph",
            "BERTScore_Precision",
        ),
        (
            "src.models.loss.agg.bertscore_f1.BERTScoreRecallGraph",
            "BERTScore_Recall",
        ),
    ],
)
def test_log_hyperparameters_logs_canonical_bertscore_directional_aliases(
    capture_logger,
    logging_runtime,
    target: str,
    expected: str,
) -> None:
    trainer, model = logging_runtime
    cfg = _build_cfg(
        {
            "contrastive": {
                "model": {
                    "loss_fn": {
                        "_target_": "src.models.loss.mxclr.MXCLR",
                        "agg": {
                            "_target_": target,
                            "transport_lambda": 0.5,
                        },
                    }
                }
            },
            "classification": {"trainer": {"max_epochs": 40}},
            "data": {"dataset_name": "aapd"},
            "callbacks": {},
            "extras": {},
            "task_name": "train",
            "tags": ["dev"],
            "seed": 0,
        }
    )

    log_hyperparameters(
        {
            "cfg": cfg,
            "stage_name": "contrastive",
            "model": model,
            "trainer": trainer,
        }
    )

    assert capture_logger.logged is not None
    assert capture_logger.logged["contrastive"]["model"]["loss_fn"]["agg_name"] == expected


def test_log_hyperparameters_derives_aliases_from_stage_runtime_loss_target(
    capture_logger,
    logging_runtime,
) -> None:
    trainer, model = logging_runtime
    cfg = _build_cfg(
        {
            "contrastive": {
                "model": {
                    "loss_fn": {
                        "_target_": "src.models.loss.mxclr.MXCLR",
                    }
                }
            },
            "classification": {"trainer": {"max_epochs": 40}},
            "data": {"dataset_name": "aapd"},
            "callbacks": {},
            "extras": {},
            "task_name": "train",
            "tags": ["dev"],
            "seed": 0,
        }
    )
    stage_cfg = _build_cfg(
        {
            "model": {
                "loss_fn": {
                    "_target_": "src.models.loss.mxclr_proto.MXCLRProto",
                    "agg": {
                        "_target_": "src.models.loss.agg.bertscore_f1.BERTScoreF1Graph",
                    },
                    "graph_temperature_schedule": {
                        "start": 0.4,
                        "end": 0.1,
                    },
                }
            }
        }
    )

    log_hyperparameters(
        {
            "cfg": cfg,
            "stage_name": "contrastive",
            "stage_cfg": stage_cfg,
            "model": model,
            "trainer": trainer,
        }
    )

    assert capture_logger.logged is not None
    assert capture_logger.logged["contrastive"]["model"]["loss_name"] == "mxclr_proto"
    assert capture_logger.logged["contrastive"]["model"]["loss_fn"]["agg_name"] == "BERTScore_F1"
    assert capture_logger.logged["contrastive"]["model"]["loss_fn"]["graph_temperature"] == 0.4
