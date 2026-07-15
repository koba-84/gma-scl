from __future__ import annotations

import copy
from typing import Any

_CLASSIFICATION_LOSS_NAME_BY_TARGET = {
    "src.models.loss.classification.AsymmetricLoss": "asymmetric",
    "src.models.loss.classification.ZLPRLoss": "zlpr",
    "torch.nn.BCEWithLogitsLoss": "bce",
}

_CONTRASTIVE_AGG_NAME_BY_TARGET = {
    "src.models.loss.agg.bertscore_f1.BERTScoreF1Graph": "BERTScore_F1",
    "src.models.loss.agg.bertscore_f1.BERTScoreUniformF1Graph": "BERTScore_F1_Uniform",
    "src.models.loss.agg.bertscore_f1.BERTScorePrecisionGraph": "BERTScore_Precision",
    "src.models.loss.agg.bertscore_f1.BERTScoreRecallGraph": "BERTScore_Recall",
}

_MXCLR_PROTO_TARGET = "src.models.loss.mxclr_proto.MXCLRProto"


def _get_nested(config: dict[str, Any], path: tuple[str, ...]) -> Any:
    current: Any = config
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def _set_nested(config: dict[str, Any], path: tuple[str, ...], value: Any) -> None:
    current = config
    for key in path[:-1]:
        current = current.setdefault(key, {})
    current[path[-1]] = value


def merge_nested_config(base: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge nested config subtrees without mutating the inputs."""
    merged = copy.deepcopy(base)

    for key, value in extra.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_nested_config(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)

    return merged


def _derive_contrastive_loss_name(target: str) -> str | None:
    parts = target.split(".")
    if len(parts) < 2:
        return None

    module_name = parts[-2]
    if not module_name or module_name == "classification":
        return None

    return module_name


def _derive_contrastive_agg_name(target: str) -> str | None:
    alias = _CONTRASTIVE_AGG_NAME_BY_TARGET.get(target)
    if alias is not None:
        return alias

    parts = target.split(".")
    if len(parts) < 2:
        return None

    module_name = parts[-2]
    if not module_name or module_name == "agg":
        return None

    return module_name


def derive_wandb_config_aliases(config: dict[str, Any]) -> dict[str, Any]:
    """Derive nested W&B comparison aliases from a resolved training config."""
    aliases: dict[str, Any] = {}

    contrastive_target = _get_nested(config, ("contrastive", "model", "loss_fn", "_target_"))
    if isinstance(contrastive_target, str):
        loss_name = _derive_contrastive_loss_name(contrastive_target)
        if loss_name is not None:
            _set_nested(aliases, ("contrastive", "model", "loss_name"), loss_name)

    contrastive_agg_target = _get_nested(
        config, ("contrastive", "model", "loss_fn", "agg", "_target_")
    )
    if isinstance(contrastive_agg_target, str):
        agg_name = _derive_contrastive_agg_name(contrastive_agg_target)
        if agg_name is not None:
            _set_nested(aliases, ("contrastive", "model", "loss_fn", "agg_name"), agg_name)

    graph_temperature = _get_nested(
        config, ("contrastive", "model", "loss_fn", "graph_temperature")
    )
    if graph_temperature is None and contrastive_target == _MXCLR_PROTO_TARGET:
        graph_temperature = _get_nested(
            config,
            ("contrastive", "model", "loss_fn", "graph_temperature_schedule", "start"),
        )
    if graph_temperature is not None:
        _set_nested(
            aliases,
            ("contrastive", "model", "loss_fn", "graph_temperature"),
            graph_temperature,
        )

    classification_target = _get_nested(
        config, ("classification", "model", "criterion", "_target_")
    )
    if isinstance(classification_target, str):
        loss_name = _CLASSIFICATION_LOSS_NAME_BY_TARGET.get(classification_target)
        if loss_name is not None:
            _set_nested(aliases, ("classification", "model", "loss_name"), loss_name)

    return aliases
