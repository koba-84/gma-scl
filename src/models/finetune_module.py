from collections.abc import Callable
from pathlib import Path
from typing import Any, cast

import torch
from lightning import LightningModule
from torch.optim.lr_scheduler import LRScheduler
from torchmetrics import MeanMetric, MetricCollection
from torchmetrics.classification import MultilabelAveragePrecision
from torchmetrics.classification.f_beta import F1Score
from torchmetrics.classification.hamming import HammingDistance

OptimizerFactory = Callable[..., torch.optim.Optimizer]
SchedulerFactory = Callable[..., LRScheduler]
ModelInput = torch.Tensor | dict[str, torch.Tensor]
BatchInput = dict[str, torch.Tensor]
BatchType = tuple[BatchInput, torch.Tensor]


def _threshold_metric_collection(num_classes: int, prefix: str) -> MetricCollection:
    return MetricCollection(
        {
            "f1_macro": F1Score(task="multilabel", num_labels=num_classes, average="macro"),
            "f1_micro": F1Score(task="multilabel", num_labels=num_classes, average="micro"),
            "hamming_loss": HammingDistance(task="multilabel", num_labels=num_classes),
        },
        prefix=prefix,
    )


def _ranking_metric_collection(num_classes: int, prefix: str) -> MetricCollection:
    return MetricCollection(
        {
            "map": MultilabelAveragePrecision(num_labels=num_classes, average="macro"),
        },
        prefix=prefix,
    )


class FinetuneLitModule(LightningModule):
    """LightningModule for classification finetuning with optional encoder freezing."""

    def __init__(
        self,
        encoder: torch.nn.Module,
        optimizer: OptimizerFactory,
        scheduler: SchedulerFactory | None,
        num_classes: int,
        criterion: torch.nn.Module,
        encoder_freeze: bool = True,
        pretrained_encoder_path: str | None = None,
        compile: bool = False,
    ) -> None:
        super().__init__()
        self.save_hyperparameters(logger=False, ignore=["encoder", "criterion"])

        self.encoder = encoder
        self.encoder_freeze = encoder_freeze
        self.pretrained_encoder_path = pretrained_encoder_path

        if not hasattr(encoder, "hidden_size"):
            raise ValueError("encoder must expose hidden_size for classifier input size.")
        hidden_size = int(getattr(encoder, "hidden_size"))
        self.classifier = torch.nn.Linear(hidden_size, num_classes)

        self.criterion = criterion

        self.train_loss = MeanMetric()
        self.val_loss = MeanMetric()
        self.test_loss = MeanMetric()
        self.val_threshold_metrics = _threshold_metric_collection(
            num_classes, "classification/val/"
        )
        self.val_ranking_metrics = _ranking_metric_collection(num_classes, "classification/val/")
        self.test_threshold_metrics = _threshold_metric_collection(
            num_classes, "classification/test/"
        )
        self.test_ranking_metrics = _ranking_metric_collection(num_classes, "classification/test/")
        self._test_prediction_scores: list[torch.Tensor] = []
        self._test_prediction_targets: list[torch.Tensor] = []

    def forward(self, x: ModelInput) -> torch.Tensor:
        """Run the forward computation and return model outputs."""
        features = cast(torch.Tensor, self.encoder(x))
        return self.classifier(features)

    def on_train_start(self) -> None:
        """Reset validation metrics at training start."""
        self.val_loss.reset()
        self.val_threshold_metrics.reset()
        self.val_ranking_metrics.reset()

    def on_fit_start(self) -> None:
        """Validate setup and apply encoder initialization policy."""
        self._configure_stage_metric_axes()
        encoder_pretrained = getattr(self.encoder, "load_pretrained_weights", None)
        if (
            self.encoder_freeze
            and not self.pretrained_encoder_path
            and encoder_pretrained is False
        ):
            raise RuntimeError(
                "Invalid finetune config: encoder_freeze=True with randomly initialized encoder. "
                "Set classification.model.pretrained_encoder_path or enable "
                "classification.model.encoder.load_pretrained_weights=true, "
                "or set classification.model.encoder_freeze=false."
            )
        if self.pretrained_encoder_path:
            self._load_pretrained_encoder(self.pretrained_encoder_path)
        self._set_encoder_trainable(not self.encoder_freeze)

    def _configure_stage_metric_axes(self) -> None:
        if self.trainer is None:
            return
        for logger in self.trainer.loggers:
            experiment = getattr(logger, "experiment", None)
            define_metric = getattr(experiment, "define_metric", None)
            if callable(define_metric):
                define_metric("classification/epoch")
                define_metric("classification/train/*", step_metric="classification/epoch")
                define_metric("classification/val/*", step_metric="classification/epoch")
                define_metric("classification/test/*", step_metric="classification/epoch")

    def on_test_start(self) -> None:
        """Reset classification test prediction buffers before the test epoch."""
        self.test_loss.reset()
        self.test_threshold_metrics.reset()
        self.test_ranking_metrics.reset()
        self._test_prediction_scores = []
        self._test_prediction_targets = []

    def _iter_artifact_experiments(self) -> list[Any]:
        trainer = self.trainer
        if trainer is None:
            return []
        experiments: list[Any] = []
        for logger in getattr(trainer, "loggers", []):
            experiment = getattr(logger, "experiment", None)
            if callable(getattr(experiment, "log_artifact", None)):
                experiments.append(experiment)
        return experiments

    def _classification_test_prediction_dir(self) -> Path | None:
        experiments = self._iter_artifact_experiments()
        if not experiments:
            return None
        trainer = self.trainer
        if trainer is None:
            return None
        root_dir = getattr(trainer, "default_root_dir", ".")
        artifact_dir = Path(str(root_dir)) / "artifacts" / "classification_test_predictions"
        artifact_dir.mkdir(parents=True, exist_ok=True)
        return artifact_dir

    def _log_test_prediction_artifacts(
        self,
        artifact_path: Path,
        scores: torch.Tensor,
        targets: torch.Tensor,
    ) -> None:
        import wandb

        for experiment in self._iter_artifact_experiments():
            run_id = getattr(experiment, "id", None)
            artifact_name = (
                f"{run_id}-classification-test-predictions"
                if isinstance(run_id, str) and run_id
                else "classification-test-predictions"
            )
            artifact = wandb.Artifact(
                name=artifact_name,
                type="classification_test_predictions",
                description=(
                    "Sigmoid classification test scores paired with ground-truth multilabel targets."
                ),
                metadata={
                    "stage": "classification/test",
                    "format": "torch.save",
                    "num_examples": int(scores.shape[0]),
                    "num_classes": int(scores.shape[1]),
                },
            )
            artifact.add_file(str(artifact_path), name=artifact_path.name)
            experiment.log_artifact(artifact)

    def on_test_end(self) -> None:
        """Persist classification test scores and targets as a W&B artifact when available."""
        artifact_dir = self._classification_test_prediction_dir()
        if artifact_dir is None or not self._test_prediction_scores:
            return

        local_scores = torch.cat(self._test_prediction_scores, dim=0)
        local_targets = torch.cat(self._test_prediction_targets, dim=0)

        trainer = self.trainer
        if trainer is None:
            return
        rank = int(getattr(trainer, "global_rank", 0))
        world_size = int(getattr(trainer, "world_size", 1))
        shard_path = artifact_dir / f"classification_test_predictions.rank{rank}.pt"
        torch.save(
            {"scores": local_scores, "targets": local_targets},
            shard_path,
        )

        barrier = getattr(getattr(trainer, "strategy", None), "barrier", None)
        if callable(barrier):
            barrier()
        if rank != 0:
            return

        shard_payloads: list[dict[str, torch.Tensor]] = []
        for shard_rank in range(world_size):
            candidate = artifact_dir / f"classification_test_predictions.rank{shard_rank}.pt"
            if candidate.exists():
                payload = torch.load(candidate, map_location="cpu", weights_only=False)
                shard_payloads.append(cast(dict[str, torch.Tensor], payload))

        if not shard_payloads:
            return

        scores = torch.cat([payload["scores"] for payload in shard_payloads], dim=0)
        targets = torch.cat([payload["targets"] for payload in shard_payloads], dim=0)
        artifact_path = artifact_dir / "classification_test_predictions.pt"
        torch.save({"scores": scores, "targets": targets}, artifact_path)
        self._log_test_prediction_artifacts(artifact_path, scores, targets)

        for shard_rank in range(world_size):
            candidate = artifact_dir / f"classification_test_predictions.rank{shard_rank}.pt"
            if candidate.exists():
                candidate.unlink()

    def _load_pretrained_encoder(self, ckpt_path: str) -> None:
        ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
        state_dict = ckpt.get("state_dict", ckpt)
        encoder_state = {
            k.removeprefix("encoder."): v
            for k, v in state_dict.items()
            if k.startswith("encoder.")
        }
        missing, unexpected = self.encoder.load_state_dict(encoder_state, strict=False)
        if missing or unexpected:
            raise RuntimeError(
                f"Pretrained encoder state mismatch. Missing: {len(missing)}, "
                f"Unexpected: {len(unexpected)}"
            )

    def _set_encoder_trainable(self, trainable: bool) -> None:
        for param in self.encoder.parameters():
            param.requires_grad = trainable

    def model_step(
        self, batch: BatchType
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """Compute classification loss, scores, and predictions for one batch."""
        x, y = batch
        y = y.float()
        logits = self.forward(x)
        loss = self.criterion(logits, y)
        scores = torch.sigmoid(logits)
        preds = (scores >= 0.5).int()
        targets = y.int()
        return loss, scores, preds, targets

    @staticmethod
    def _apply_empty_text_override(preds: torch.Tensor, inputs: BatchInput) -> torch.Tensor:
        """Set prediction rows to zero for empty-text samples."""
        empty_mask = inputs.get("empty_text_mask")
        if isinstance(empty_mask, torch.Tensor):
            empty_mask = empty_mask.to(device=preds.device, dtype=torch.bool)
            if torch.any(empty_mask):
                preds[empty_mask] = 0
        return preds

    def training_step(self, batch: BatchType, _: int) -> torch.Tensor:
        """Run one training step and log train loss."""
        loss, _scores, _preds, _targets = self.model_step(batch)
        self.train_loss(loss)
        batch_size = int(batch[1].size(0))
        self.log(
            "classification/epoch",
            float(self.current_epoch),
            on_step=False,
            on_epoch=True,
            batch_size=batch_size,
        )
        self.log(
            "classification/train/loss",
            self.train_loss,
            on_step=False,
            on_epoch=True,
            prog_bar=True,
        )
        return loss

    def validation_step(self, batch: BatchType, _: int) -> None:
        """Run one validation step and log validation metrics."""
        loss, scores, preds, targets = self.model_step(batch)
        self.val_loss(loss)
        self.val_threshold_metrics.update(preds, targets)
        self.val_ranking_metrics.update(scores, targets)

    def on_validation_epoch_end(self) -> None:
        """Log validation metrics at epoch end via MetricCollection outputs."""
        self.log(
            "classification/epoch",
            float(self.current_epoch),
            on_step=False,
            on_epoch=True,
        )
        self.log(
            "classification/val/loss",
            self.val_loss.compute(),
            on_step=False,
            on_epoch=True,
            prog_bar=True,
        )
        self.log_dict(
            self.val_threshold_metrics.compute() | self.val_ranking_metrics.compute(),
            on_step=False,
            on_epoch=True,
        )
        self.val_loss.reset()
        self.val_threshold_metrics.reset()
        self.val_ranking_metrics.reset()

    def test_step(self, batch: BatchType, _: int) -> None:
        """Run one test step and log test metrics."""
        loss, scores, preds, targets = self.model_step(batch)
        inputs, _labels = batch
        preds = self._apply_empty_text_override(preds, inputs)
        self.test_loss(loss)
        self.test_threshold_metrics.update(preds, targets)
        self.test_ranking_metrics.update(scores, targets)
        self._test_prediction_scores.append(scores.detach().cpu())
        self._test_prediction_targets.append(targets.detach().cpu())

    def on_test_epoch_end(self) -> None:
        """Log test metrics at epoch end via MetricCollection outputs."""
        self.log(
            "classification/epoch",
            float(self.current_epoch),
            on_step=False,
            on_epoch=True,
        )
        self.log_dict(
            self.test_threshold_metrics.compute() | self.test_ranking_metrics.compute(),
            on_step=False,
            on_epoch=True,
        )
        self.test_loss.reset()
        self.test_threshold_metrics.reset()
        self.test_ranking_metrics.reset()

    def setup(self, stage: str) -> None:
        """Set up compile path for fit stage."""
        trainer = self.trainer
        root_device = None if trainer is None else getattr(trainer.strategy, "root_device", None)
        compile_enabled = (
            stage == "fit"
            and bool(getattr(self.hparams, "compile", False))
            and getattr(root_device, "type", "cpu") != "cpu"
        )
        if compile_enabled:
            self.encoder = cast(torch.nn.Module, torch.compile(self.encoder))
            self.classifier = cast(torch.nn.Linear, torch.compile(self.classifier))

    def configure_optimizers(self) -> Any:
        """Configure optimizer and optional scheduler."""
        hparams = cast(Any, self.hparams)
        optimizer = hparams.optimizer(params=[p for p in self.parameters() if p.requires_grad])
        if hparams.scheduler is not None:
            scheduler = hparams.scheduler(optimizer=optimizer)
            return {
                "optimizer": optimizer,
                "lr_scheduler": {
                    "scheduler": scheduler,
                    "monitor": "classification/val/loss",
                    "interval": "epoch",
                    "frequency": 1,
                },
            }
        return {"optimizer": optimizer}


if __name__ == "__main__":
    encoder = torch.nn.Identity()
    setattr(encoder, "hidden_size", 10)
    _ = FinetuneLitModule(
        encoder=encoder,
        optimizer=torch.optim.Adam,
        scheduler=None,
        num_classes=4,
        criterion=torch.nn.BCEWithLogitsLoss(),
    )
