from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest


def _load_backfill_module() -> ModuleType:
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "backfill_wandb_config.py"
    spec = importlib.util.spec_from_file_location("test_backfill_wandb_config_module", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load backfill_wandb_config.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_MODULE = _load_backfill_module()
build_backfill_payload = _MODULE.build_backfill_payload
inflate_flat_root_keys = _MODULE._inflate_flat_root_keys
merge_backfill_source_config = _MODULE.merge_backfill_source_config
normalize_downloaded_run_config = _MODULE.normalize_downloaded_run_config


def test_build_backfill_payload_adds_missing_contrastive_loss_name_alias() -> None:
    payload = build_backfill_payload(
        {
            "contrastive": "__replace_contrastive__",
        },
        {
            "contrastive": {
                "model": {
                    "loss_fn": {
                        "_target_": "src.models.loss.mxclr.build_from_data",
                        "instance_temperature": 0.1,
                    },
                    "loss_name": "mxclr",
                }
            }
        },
    )

    assert payload["contrastive"]["model"]["loss_name"] == "mxclr"


def test_build_backfill_payload_keeps_existing_contrastive_loss_name_alias() -> None:
    payload = build_backfill_payload(
        {
            "contrastive": {
                "model": {
                    "loss_fn": {
                        "_target_": "src.models.loss.mxclr.build_from_data",
                        "instance_temperature": 0.1,
                    },
                    "loss_name": "mxclr",
                }
            },
        },
        {
            "contrastive": {
                "model": {
                    "loss_fn": {
                        "_target_": "src.models.loss.mxclr.build_from_data",
                        "instance_temperature": 0.1,
                    },
                    "loss_name": "mxclr",
                }
            }
        },
    )

    assert payload == {}


def test_build_backfill_payload_adds_missing_mxclr_proto_aliases() -> None:
    payload = build_backfill_payload(
        {
            "contrastive": "__replace_contrastive__",
        },
        {
            "contrastive": {
                "model": {
                    "loss_fn": {
                        "_target_": "src.models.loss.mxclr_proto.MXCLRProto",
                        "agg": {
                            "_target_": "src.models.loss.agg.bertscore_f1.BERTScoreF1Graph",
                        },
                        "graph_temperature_schedule": {
                            "start": 0.5,
                            "end": 0.1,
                        },
                    }
                }
            }
        },
    )

    assert payload["contrastive"]["model"]["loss_name"] == "mxclr_proto"
    assert payload["contrastive"]["model"]["loss_fn"]["agg"]["_target_"] == (
        "src.models.loss.agg.bertscore_f1.BERTScoreF1Graph"
    )
    assert payload["contrastive"]["model"]["loss_fn"]["agg_name"] == "BERTScore_F1"
    assert payload["contrastive"]["model"]["loss_fn"]["graph_temperature"] == 0.5


def test_build_backfill_payload_preserves_canonical_bertscore_f1_alias() -> None:
    payload = build_backfill_payload(
        {
            "contrastive": "__replace_contrastive__",
        },
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
            }
        },
    )

    assert payload["contrastive"]["model"]["loss_fn"]["agg_name"] == "BERTScore_F1"


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
def test_build_backfill_payload_preserves_canonical_bertscore_directional_aliases(
    target: str,
    expected: str,
) -> None:
    payload = build_backfill_payload(
        {
            "contrastive": "__replace_contrastive__",
        },
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
            }
        },
    )

    assert payload["contrastive"]["model"]["loss_fn"]["agg_name"] == expected


def test_normalize_downloaded_run_config_restores_replaced_contrastive_root() -> None:
    normalized = normalize_downloaded_run_config(
        {
            "_items": {
                "value": {
                    "contrastive": {
                        "model": {
                            "loss_fn": {
                                "_target_": "src.models.loss.mxclr.build_from_data",
                            },
                            "loss_name": "mxclr",
                        }
                    }
                }
            },
            "contrastive": {"value": "__replace_contrastive__"},
            "seed": {"value": 0},
        }
    )

    assert normalized["contrastive"]["model"]["loss_name"] == "mxclr"
    assert normalized["seed"] == 0


def test_merge_backfill_source_config_prefers_downloaded_nested_stage_config() -> None:
    merged = merge_backfill_source_config(
        {
            "contrastive": "__replace_contrastive__",
        },
        {
            "contrastive": {
                "model": {
                    "loss_fn": {
                        "_target_": "src.models.loss.mxclr.build_from_data",
                    },
                    "loss_name": "mxclr",
                }
            }
        },
    )

    assert merged["contrastive"]["model"]["loss_name"] == "mxclr"


def test_inflate_flat_root_keys_restores_nested_callbacks_subtree() -> None:
    inflated = inflate_flat_root_keys(
        {
            "callbacks": "__replace_callbacks__",
            "callbacks.early_stopping.patience": 5,
            "callbacks.early_stopping.mode": "min",
        }
    )

    assert inflated["callbacks"]["early_stopping"]["patience"] == 5
    assert inflated["callbacks"]["early_stopping"]["mode"] == "min"


def test_inflate_flat_root_keys_overwrites_scalar_intermediate_nodes() -> None:
    inflated = inflate_flat_root_keys(
        {
            "contrastive": {"model": "mxclr"},
            "contrastive.model.loss_name": "mxclr",
        }
    )

    assert inflated["contrastive"]["model"]["loss_name"] == "mxclr"
