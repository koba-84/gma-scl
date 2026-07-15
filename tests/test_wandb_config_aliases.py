from __future__ import annotations

from pathlib import Path

import pytest
import yaml  # type: ignore[import-untyped]

from src.utils.wandb_config_aliases import derive_wandb_config_aliases, merge_nested_config

_ROOT = Path(__file__).resolve().parents[1]


def _load_yaml(path: Path) -> dict[str, object]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise AssertionError(f"expected mapping config in {path}")
    return payload


def test_merge_nested_config_recursively_merges_subtrees() -> None:
    merged = merge_nested_config(
        {
            "contrastive": {
                "model": {
                    "loss_fn": {
                        "_target_": "src.models.loss.mxclr_proto.MXCLRProto",
                    }
                }
            }
        },
        {
            "contrastive": {
                "model": {
                    "loss_name": "mxclr_proto",
                }
            }
        },
    )

    assert merged["contrastive"]["model"]["loss_fn"]["_target_"] == (
        "src.models.loss.mxclr_proto.MXCLRProto"
    )
    assert merged["contrastive"]["model"]["loss_name"] == "mxclr_proto"


def test_derive_wandb_config_aliases_derives_contrastive_loss_from_target_module() -> None:
    aliases = derive_wandb_config_aliases(
        {
            "contrastive": {
                "model": {
                    "loss_fn": {
                        "_target_": "src.models.loss.mxclr_proto.MXCLRProto",
                    }
                }
            }
        }
    )

    assert aliases["contrastive"]["model"]["loss_name"] == "mxclr_proto"


def test_derive_wandb_config_aliases_derives_agg_and_graph_temperature_aliases() -> None:
    aliases = derive_wandb_config_aliases(
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
            }
        }
    )

    assert aliases["contrastive"]["model"]["loss_fn"]["agg_name"] == "BERTScore_F1"
    assert aliases["contrastive"]["model"]["loss_fn"]["graph_temperature"] == 0.5


def test_derive_wandb_config_aliases_does_not_use_legacy_tau_schedule() -> None:
    aliases = derive_wandb_config_aliases(
        {
            "contrastive": {
                "model": {
                    "loss_fn": {
                        "_target_": "src.models.loss.mxclr_proto.MXCLRProto",
                        "agg": {
                            "_target_": "src.models.loss.agg.bertscore_f1.BERTScoreF1Graph",
                            "transport_lambda": 0.5,
                        },
                        "tau_s_schedule": {
                            "start": 0.5,
                            "end": 0.1,
                        },
                    }
                }
            }
        }
    )

    assert aliases["contrastive"]["model"]["loss_fn"]["agg_name"] == "BERTScore_F1"
    assert "graph_temperature" not in aliases["contrastive"]["model"]["loss_fn"]


def test_derive_wandb_config_aliases_preserves_canonical_bertscore_f1_name() -> None:
    aliases = derive_wandb_config_aliases(
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
        }
    )

    assert aliases["contrastive"]["model"]["loss_fn"]["agg_name"] == "BERTScore_F1"


def test_derive_wandb_config_aliases_preserves_canonical_bertscore_uniform_f1_name() -> None:
    aliases = derive_wandb_config_aliases(
        {
            "contrastive": {
                "model": {
                    "loss_fn": {
                        "_target_": "src.models.loss.mxclr.MXCLR",
                        "agg": {
                            "_target_": (
                                "src.models.loss.agg.bertscore_f1.BERTScoreUniformF1Graph"
                            ),
                            "transport_lambda": 0.5,
                        },
                    }
                }
            }
        }
    )

    assert aliases["contrastive"]["model"]["loss_fn"]["agg_name"] == "BERTScore_F1_Uniform"


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
def test_derive_wandb_config_aliases_preserves_canonical_bertscore_directional_names(
    target: str,
    expected: str,
) -> None:
    aliases = derive_wandb_config_aliases(
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
        }
    )

    assert aliases["contrastive"]["model"]["loss_fn"]["agg_name"] == expected


def test_derive_wandb_config_aliases_preserves_mxclr_agg_subtree() -> None:
    config = {
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
        }
    }

    merged = merge_nested_config(config, derive_wandb_config_aliases(config))

    assert merged["contrastive"]["model"]["loss_fn"]["agg"]["transport_lambda"] == 0.5
    assert merged["contrastive"]["model"]["loss_fn"]["agg_name"] == "BERTScore_F1"


def test_derive_wandb_config_aliases_keeps_classification_loss_mapping() -> None:
    aliases = derive_wandb_config_aliases(
        {
            "classification": {
                "model": {
                    "criterion": {
                        "_target_": "torch.nn.BCEWithLogitsLoss",
                    }
                }
            }
        }
    )

    assert aliases["classification"]["model"]["loss_name"] == "bce"


def test_derive_wandb_config_aliases_covers_all_supported_contrastive_losses() -> None:
    config_dir = _ROOT / "configs" / "contrastive" / "model"
    for path in sorted(config_dir.glob("*.yaml")):
        if path.stem in {"base", "default"}:
            continue
        config = _load_yaml(path)
        loss_fn = config.get("loss_fn")
        if not isinstance(loss_fn, dict) or not isinstance(loss_fn.get("_target_"), str):
            raise AssertionError(f"loss target missing in {path}")
        aliases = derive_wandb_config_aliases({"contrastive": {"model": config}})
        assert aliases["contrastive"]["model"]["loss_name"] == path.stem


def test_derive_wandb_config_aliases_covers_all_supported_mxclr_aggs() -> None:
    config_dir = _ROOT / "configs" / "contrastive" / "model" / "agg"
    for path in sorted(config_dir.glob("*.yaml")):
        config = _load_yaml(path)
        agg = config.get("agg")
        if not isinstance(agg, dict) or not isinstance(agg.get("_target_"), str):
            raise AssertionError(f"agg target missing in {path}")
        aliases = derive_wandb_config_aliases(
            {
                "contrastive": {
                    "model": {
                        "loss_fn": {
                            "_target_": "src.models.loss.mxclr.MXCLR",
                            "agg": agg,
                        }
                    }
                }
            }
        )
        assert aliases["contrastive"]["model"]["loss_fn"]["agg_name"] == path.stem


def test_derive_wandb_config_aliases_covers_all_supported_classification_losses() -> None:
    config_dir = _ROOT / "configs" / "classification" / "loss"
    for path in sorted(config_dir.glob("*.yaml")):
        config = _load_yaml(path)
        criterion = config.get("criterion")
        if not isinstance(criterion, dict) or not isinstance(criterion.get("_target_"), str):
            raise AssertionError(f"classification target missing in {path}")
        aliases = derive_wandb_config_aliases({"classification": {"model": config}})
        assert aliases["classification"]["model"]["loss_name"] == path.stem
