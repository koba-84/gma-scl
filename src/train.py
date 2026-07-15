import os
from typing import Any

import hydra
import lightning as lightning
import rootutils
import torch
from lightning import Callback, LightningDataModule, LightningModule, Trainer
from lightning.pytorch.loggers import Logger
from omegaconf import DictConfig, OmegaConf

torch.set_float32_matmul_precision("high")

rootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
# ------------------------------------------------------------------------------------ #
# the setup_root above is equivalent to:
# - adding project root dir to PYTHONPATH
#       (so you don't need to force user to install project as a package)
#       (necessary before importing any local modules e.g. `from src import utils`)
# - setting up PROJECT_ROOT environment variable
#       (which is used as a base for paths in "configs/paths/default.yaml")
#       (this way all filepaths are the same no matter where you run the code)
# - loading environment variables from ".env" in root dir
#
# you can remove it if you:
# 1. either install project as a package or move entry files to project root dir
# 2. set `root_dir` to "." in "configs/paths/default.yaml"
#
# more info: https://github.com/ashleve/rootutils
# ------------------------------------------------------------------------------------ #

from src.utils import (
    RankedLogger,
    extras,
    get_metric_value,
    instantiate_callbacks,
    instantiate_loggers,
    log_hyperparameters,
    task_wrapper,
)

log = RankedLogger(__name__, rank_zero_only=True)


def _force_full_checkpoint_load_for_trusted_sources() -> None:
    """Ensure Lightning checkpoint loads use full pickle when callsites don't pass weights_only.

    This is intended for trusted checkpoints only.
    """
    if os.environ.get("TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD") != "1":
        os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"
        log.info("Set TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1 for trusted checkpoint loading.")


def _ignore_wandb_ckpt_artifacts() -> None:
    """Prevent wandb from copying ckpt files into its run directory."""
    key = "WANDB_IGNORE_GLOBS"
    pattern = "*.ckpt"
    current = os.environ.get(key, "")
    if pattern in current.split(","):
        return
    os.environ[key] = f"{current},{pattern}".strip(",")
    log.info(f"Set {key}={os.environ[key]}")


def _run_stage(
    stage_name: str, stage_cfg: DictConfig, base_cfg: DictConfig
) -> tuple[dict[str, Any], dict[str, Any], Trainer]:
    """Run a single training stage."""
    log.info(f"[{stage_name}] Instantiating datamodule <{stage_cfg.data._target_}>")
    datamodule: LightningDataModule = hydra.utils.instantiate(stage_cfg.data)

    log.info(f"[{stage_name}] Instantiating model <{stage_cfg.model._target_}>")
    model: LightningModule = hydra.utils.instantiate(stage_cfg.model)

    log.info(f"[{stage_name}] Instantiating callbacks...")
    callbacks_cfg = stage_cfg.get("callbacks", base_cfg.get("callbacks"))
    callbacks: list[Callback] = instantiate_callbacks(callbacks_cfg)

    log.info(f"[{stage_name}] Instantiating loggers...")
    logger: list[Logger] = instantiate_loggers(base_cfg.get("logger"))

    stage_trainer_cfg = stage_cfg.get("trainer")
    base_trainer_cfg = base_cfg.get("trainer")
    if stage_trainer_cfg is None:
        trainer_cfg = base_trainer_cfg
    elif stage_trainer_cfg.get("_target_") is None and base_trainer_cfg is not None:
        # Allow stage-specific overrides without redefining the trainer target.
        trainer_cfg = OmegaConf.merge(base_trainer_cfg, stage_trainer_cfg)
    else:
        trainer_cfg = stage_trainer_cfg

    stage_cfg_for_logging = OmegaConf.create(OmegaConf.to_container(stage_cfg, resolve=False))
    if trainer_cfg is not None:
        stage_cfg_for_logging.trainer = trainer_cfg
    stage_cfg_for_logging.callbacks = callbacks_cfg

    log.info(f"[{stage_name}] Instantiating trainer <{trainer_cfg._target_}>")
    trainer: Trainer = hydra.utils.instantiate(trainer_cfg, callbacks=callbacks, logger=logger)

    object_dict = {
        "cfg": base_cfg,
        "stage_name": stage_name,
        "stage_cfg": stage_cfg_for_logging,
        "datamodule": datamodule,
        "model": model,
        "callbacks": callbacks,
        "logger": logger,
        "trainer": trainer,
    }

    if logger:
        log.info(f"[{stage_name}] Logging hyperparameters!")
        log_hyperparameters(object_dict)

    if stage_cfg.get("train", True):
        log.info(f"[{stage_name}] Starting training!")
        trainer.fit(model=model, datamodule=datamodule, ckpt_path=stage_cfg.get("ckpt_path"))

    train_metrics = trainer.callback_metrics

    if stage_cfg.get("test", False):
        log.info(f"[{stage_name}] Starting testing!")
        ckpt_path = None
        ckpt_cb = getattr(trainer, "checkpoint_callback", None)
        if ckpt_cb is not None:
            ckpt_path = ckpt_cb.best_model_path or None
        if ckpt_path is None:
            log.warning(
                f"[{stage_name}] Best ckpt not found! Using current weights for testing..."
            )
        trainer.test(model=model, datamodule=datamodule, ckpt_path=ckpt_path)
        log.info(f"[{stage_name}] Best ckpt path: {ckpt_path}")
        paths_to_delete = []
        if ckpt_path:
            paths_to_delete.append(ckpt_path)
        if ckpt_cb is not None and getattr(ckpt_cb, "dirpath", None):
            last_ckpt = os.path.join(ckpt_cb.dirpath, "last.ckpt")
            paths_to_delete.append(last_ckpt)
        for path in paths_to_delete:
            try:
                os.remove(path)
                log.info(f"[{stage_name}] Deleted ckpt: {path}")
            except FileNotFoundError:
                log.warning(f"[{stage_name}] Ckpt already deleted: {path}")
            except OSError as exc:
                log.warning(f"[{stage_name}] Failed to delete ckpt: {path} ({exc})")

    test_metrics = trainer.callback_metrics
    metric_dict = {**train_metrics, **test_metrics}

    return metric_dict, object_dict, trainer


@task_wrapper
def train(cfg: DictConfig) -> tuple[dict[str, Any], dict[str, Any]]:
    """Trains the model. Can additionally evaluate on a testset, using best weights obtained during
    training.

    This method is wrapped in optional @task_wrapper decorator, that controls the behavior during
    failure. Useful for multiruns, saving info about the crash, etc.

    :param cfg: A DictConfig configuration composed by Hydra.
    :return: A tuple with metrics and dict with all instantiated objects.
    """
    # set seed for random number generators in pytorch, numpy and python.random
    if cfg.get("seed") is not None:
        lightning.seed_everything(cfg.seed, workers=True)

    _force_full_checkpoint_load_for_trusted_sources()
    _ignore_wandb_ckpt_artifacts()

    metric_dict: dict[str, Any] = {}
    object_dict: dict[str, Any] = {"cfg": cfg}

    pretrain_ckpt_path: str | None = None

    saved_contrastive_last = False
    contrastive_cfg = cfg.get("contrastive")
    if contrastive_cfg is not None and contrastive_cfg.get("model") is not None:
        log.info("Starting contrastive pretraining stage")
        contrastive_metrics, contrastive_objects, contrastive_trainer = _run_stage(
            "contrastive", contrastive_cfg, cfg
        )
        metric_dict.update(contrastive_metrics)
        object_dict["contrastive"] = contrastive_objects

        pretrain_ckpt_path = None
        ckpt_cb = getattr(contrastive_trainer, "checkpoint_callback", None)
        if ckpt_cb is not None:
            pretrain_ckpt_path = ckpt_cb.best_model_path or None
        if pretrain_ckpt_path is None and contrastive_cfg.get("save_last_encoder", True):
            output_dir = cfg.paths.output_dir
            ckpt_dir = os.path.join(output_dir, "checkpoints")
            os.makedirs(ckpt_dir, exist_ok=True)
            pretrain_ckpt_path = os.path.join(ckpt_dir, "contrastive_last.ckpt")
            model = contrastive_objects["model"]
            torch.save({"state_dict": model.state_dict()}, pretrain_ckpt_path)
            log.info(f"[contrastive] Saved last encoder ckpt to: {pretrain_ckpt_path}")
            saved_contrastive_last = True

    classification_cfg = cfg.get("classification")
    if classification_cfg is not None and classification_cfg.get("model") is not None:
        if pretrain_ckpt_path and not classification_cfg.model.get("pretrained_encoder_path"):
            classification_cfg.model.pretrained_encoder_path = pretrain_ckpt_path

        log.info("Starting classification stage")
        classification_metrics, classification_objects, _ = _run_stage(
            "classification", classification_cfg, cfg
        )
        metric_dict.update(classification_metrics)
        object_dict["classification"] = classification_objects
        if saved_contrastive_last and pretrain_ckpt_path:
            try:
                os.remove(pretrain_ckpt_path)
                log.info(f"[contrastive] Deleted last encoder ckpt: {pretrain_ckpt_path}")
            except FileNotFoundError:
                log.warning(
                    f"[contrastive] Last encoder ckpt already deleted: {pretrain_ckpt_path}"
                )
            except OSError as exc:
                log.warning(
                    f"[contrastive] Failed to delete last encoder ckpt: {pretrain_ckpt_path} ({exc})"
                )
    elif classification_cfg is not None:
        log.warning(
            "[classification] Config missing 'model'; skipping classification stage. "
            "Check your composed config or stage defaults."
        )

    return metric_dict, object_dict


@hydra.main(version_base="1.3", config_path="../configs", config_name="train.yaml")
def main(cfg: DictConfig) -> float | None:
    """Main entry point for training.

    :param cfg: DictConfig configuration composed by Hydra.
    :return: Optional[float] with optimized metric value.
    """
    # apply extra utilities
    # (e.g. ask for tags if none are provided in cfg, print cfg tree, etc.)
    extras(cfg)

    # train the model
    metric_dict, _ = train(cfg)

    # safely retrieve metric value for hydra-based hyperparameter optimization
    metric_value = get_metric_value(
        metric_dict=metric_dict, metric_name=cfg.get("optimized_metric")
    )

    # return optimized metric
    return metric_value


if __name__ == "__main__":
    main()
