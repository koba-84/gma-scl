from typing import Any, cast

from lightning_utilities.core.rank_zero import rank_zero_only
from omegaconf import OmegaConf

from src.utils import pylogger
from src.utils.wandb_config_aliases import derive_wandb_config_aliases, merge_nested_config

log = pylogger.RankedLogger(__name__, rank_zero_only=True)


def _resolve_logging_hparams(
    cfg: Any,
    stage_name: str | None,
    stage_cfg: Any,
) -> dict[str, Any]:
    cfg_for_logging = cast(dict[str, Any], OmegaConf.to_container(cfg, resolve=False))

    if stage_name in ("contrastive", "classification") and stage_cfg is not None:
        cfg_for_logging[stage_name] = stage_cfg

    return cast(
        dict[str, Any], OmegaConf.to_container(OmegaConf.create(cfg_for_logging), resolve=True)
    )


@rank_zero_only
def log_hyperparameters(object_dict: dict[str, Any]) -> None:
    """Controls which config parts are saved by Lightning loggers.

    Additionally saves:
        - Number of model parameters

    :param object_dict: A dictionary containing the following objects:
        - `"cfg"`: A DictConfig object containing the main config.
        - `"stage_name"`: Current stage name (`contrastive` or `classification`).
        - `"model"`: The Lightning model.
        - `"trainer"`: The Lightning trainer.
    """
    hparams: dict[str, Any] = {}

    stage_name = object_dict.get("stage_name")
    stage_cfg = object_dict.get("stage_cfg")
    model = object_dict["model"]
    trainer = object_dict["trainer"]
    cfg = _resolve_logging_hparams(object_dict["cfg"], stage_name, stage_cfg)

    if not trainer.logger:
        log.warning("Logger not found! Skipping hyperparameter logging...")
        return

    hparams["contrastive"] = cfg.get("contrastive")
    hparams["classification"] = cfg.get("classification")

    # save stage-specific model parameter counts to avoid collisions in a shared run
    if stage_name in ("contrastive", "classification"):
        hparams[f"{stage_name}/model/params/total"] = sum(p.numel() for p in model.parameters())
        hparams[f"{stage_name}/model/params/trainable"] = sum(
            p.numel() for p in model.parameters() if p.requires_grad
        )
        hparams[f"{stage_name}/model/params/non_trainable"] = sum(
            p.numel() for p in model.parameters() if not p.requires_grad
        )

    hparams["data"] = cfg.get("data")
    hparams["trainer"] = cfg.get("trainer")

    hparams["callbacks"] = cfg.get("callbacks")
    hparams["extras"] = cfg.get("extras")

    hparams["task_name"] = cfg.get("task_name")
    hparams["tags"] = cfg.get("tags")
    hparams["ckpt_path"] = cfg.get("ckpt_path")
    hparams["seed"] = cfg.get("seed")

    hparams = merge_nested_config(hparams, derive_wandb_config_aliases(hparams))

    # send hparams to all loggers
    for logger in trainer.loggers:
        logger.log_hyperparams(hparams)
