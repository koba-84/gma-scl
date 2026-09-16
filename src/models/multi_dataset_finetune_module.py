from __future__ import annotations

from collections.abc import Callable, Mapping
from math import isfinite
from pathlib import Path
from typing import Any, cast

import torch
from lightning import LightningModule
from torch.optim.lr_scheduler import LRScheduler
from torchmetrics import MeanMetric, MetricCollection
from torchmetrics.classification import MultilabelAveragePrecision
from torchmetrics.classification.f_beta import F1Score
from torchmetrics.classification.hamming import HammingDistance

from src.models.components.encoder_lifecycle import EncoderLifecycleMixin

BatchInput = dict[str, torch.Tensor]
BatchType = tuple[BatchInput, torch.Tensor]
OptimizerFactory = Callable[..., torch.optim.Optimizer]
SchedulerFactory = Callable[..., LRScheduler]


def _threshold_metrics(num_classes: int, prefix: str) -> MetricCollection:
    return MetricCollection(
        {
            "f1_macro": F1Score(task="multilabel", num_labels=num_classes, average="macro"),
            "f1_micro": F1Score(task="multilabel", num_labels=num_classes, average="micro"),
            "hamming_loss": HammingDistance(task="multilabel", num_labels=num_classes),
        },
        prefix=prefix,
    )


def _ranking_metrics(num_classes: int, prefix: str) -> MetricCollection:
    return MetricCollection(
        {"map": MultilabelAveragePrecision(num_labels=num_classes, average="macro")},
        prefix=prefix,
    )


class MultiDatasetFinetuneLitModule(EncoderLifecycleMixin, LightningModule):
    """Shared encoder with independently selected dataset-specific classifiers."""

    uses_dataset_specific_best_state = True

    def __init__(
        self,
        encoder: torch.nn.Module,
        optimizer: OptimizerFactory,
        scheduler: SchedulerFactory | None,
        dataset_names: list[str] | tuple[str, ...],
        num_classes_by_dataset: Mapping[str, int],
        label_offsets: Mapping[str, int],
        classifier_lr_by_dataset: Mapping[str, float],
        criterion: torch.nn.Module,
        encoder_freeze: bool = True,
        pretrained_encoder_path: str | None = None,
        compile: bool = False,
    ) -> None:
        super().__init__()
        names = [str(name) for name in dataset_names]
        if not names or len(set(names)) != len(names):
            raise ValueError("dataset_names must contain unique dataset names.")
        if set(names) != set(num_classes_by_dataset) or set(names) != set(label_offsets):
            raise ValueError("dataset metadata keys must match dataset_names.")
        self.save_hyperparameters(logger=False, ignore=["encoder", "criterion"])
        self.encoder = encoder
        self.encoder_freeze = bool(encoder_freeze)
        self.pretrained_encoder_path = pretrained_encoder_path
        hidden_size = int(getattr(encoder, "hidden_size", 0))
        if hidden_size <= 0:
            raise ValueError("encoder must expose a positive hidden_size.")
        self.dataset_names = tuple(names)
        self.num_classes_by_dataset = {name: int(num_classes_by_dataset[name]) for name in names}
        self.label_offsets = {name: int(label_offsets[name]) for name in names}
        if set(classifier_lr_by_dataset) != set(names):
            raise ValueError("classifier_lr_by_dataset keys must match dataset_names.")
        self.classifier_lr_by_dataset = {}
        for name in names:
            learning_rate = float(classifier_lr_by_dataset[name])
            if not isfinite(learning_rate) or learning_rate <= 0:
                raise ValueError(
                    f"classifier learning rate for '{name}' must be finite and positive."
                )
            self.classifier_lr_by_dataset[name] = learning_rate
        if any(value <= 0 for value in self.num_classes_by_dataset.values()):
            raise ValueError("Each dataset must have at least one class.")
        self.classifiers = torch.nn.ModuleDict(
            {
                name: torch.nn.Linear(hidden_size, self.num_classes_by_dataset[name])
                for name in names
            }
        )
        self.criterion = criterion
        self.train_loss = MeanMetric()
        self.val_loss = MeanMetric()
        self.test_loss = MeanMetric()
        self.val_threshold_metrics = torch.nn.ModuleDict(
            {
                name: _threshold_metrics(self.num_classes_by_dataset[name], f"{name}/")
                for name in names
            }
        )
        self.val_ranking_metrics = torch.nn.ModuleDict(
            {
                name: _ranking_metrics(self.num_classes_by_dataset[name], f"{name}/")
                for name in names
            }
        )
        self.test_threshold_metrics = torch.nn.ModuleDict(
            {
                name: _threshold_metrics(self.num_classes_by_dataset[name], f"{name}/")
                for name in names
            }
        )
        self.test_ranking_metrics = torch.nn.ModuleDict(
            {
                name: _ranking_metrics(self.num_classes_by_dataset[name], f"{name}/")
                for name in names
            }
        )
        self.best_val_macro_f1 = {name: float("-inf") for name in names}
        self.best_classifier_states: dict[str, dict[str, torch.Tensor]] = {}
        self.best_model_states: dict[str, dict[str, torch.Tensor]] = {}
        self._test_prediction_scores: dict[str, list[torch.Tensor]] = {name: [] for name in names}
        self._test_prediction_targets: dict[str, list[torch.Tensor]] = {name: [] for name in names}

    def _configure_stage_metric_axes(self) -> None:
        """Define dataset-specific metric axes for supported experiment loggers."""
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

    def _dataset_mask(self, inputs: BatchInput, dataset_id: int) -> torch.Tensor:
        ids = inputs.get("dataset_id")
        if ids is None:
            raise ValueError("multi-dataset batch must contain dataset_id.")
        return ids == dataset_id

    def _local_targets(self, labels: torch.Tensor, name: str) -> torch.Tensor:
        start = self.label_offsets[name]
        end = start + self.num_classes_by_dataset[name]
        return labels[:, start:end].float()

    def forward(self, inputs: BatchInput) -> dict[str, torch.Tensor]:
        """Return current logits grouped by dataset for a mixed batch."""
        features = cast(torch.Tensor, self.encoder(inputs))
        result: dict[str, torch.Tensor] = {}
        for dataset_id, name in enumerate(self.dataset_names):
            mask = self._dataset_mask(inputs, dataset_id)
            if torch.any(mask):
                result[name] = self.classifiers[name](features[mask])
        return result

    def model_step(
        self,
        batch: BatchType,
        *,
        use_best_classifier: bool = False,
    ) -> dict[str, tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]]:
        """Compute loss, scores, predictions, and targets separately per dataset."""
        inputs, labels = batch
        features = (
            None
            if (use_best_classifier and not self.encoder_freeze)
            else cast(torch.Tensor, self.encoder(inputs))
        )
        outputs: dict[str, tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]] = {}
        for dataset_id, name in enumerate(self.dataset_names):
            mask = self._dataset_mask(inputs, dataset_id)
            if not torch.any(mask):
                continue
            best_state = self.best_model_states.get(name) if use_best_classifier else None
            if best_state is not None and not self.encoder_freeze:
                encoder_state = {
                    key.removeprefix("encoder."): value
                    for key, value in best_state.items()
                    if key.startswith("encoder.")
                }
                self.encoder.load_state_dict(encoder_state, strict=True)
                features = cast(torch.Tensor, self.encoder(inputs))
            elif features is None:
                features = cast(torch.Tensor, self.encoder(inputs))
            if features is None:
                raise RuntimeError("Dataset features were not computed.")
            head = self.classifiers[name]
            if use_best_classifier and name in self.best_classifier_states:
                state = self.best_classifier_states[name]
                logits = torch.nn.functional.linear(
                    features[mask], state["weight"].to(features), state["bias"].to(features)
                )
            else:
                logits = head(features[mask])
            targets = self._local_targets(labels[mask], name)
            loss = self.criterion(logits, targets)
            scores = torch.sigmoid(logits)
            predictions = (scores >= 0.5).int()
            outputs[name] = (loss, scores, predictions, targets.int())
        if not outputs:
            raise ValueError("mixed batch contains no configured dataset ids.")
        return outputs

    @staticmethod
    def _mean_losses(
        outputs: Mapping[str, tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]],
    ) -> torch.Tensor:
        return torch.stack([values[0] for values in outputs.values()]).mean()

    def training_step(self, batch: BatchType, _: int) -> torch.Tensor:
        """Run one mixed-batch classification step."""
        outputs = self.model_step(batch)
        loss = self._mean_losses(outputs)
        self.train_loss(loss)
        self.log("classification/train/loss", self.train_loss, on_step=False, on_epoch=True)
        return loss

    def validation_step(self, batch: BatchType, _: int) -> None:
        """Update validation metrics independently for each dataset."""
        outputs = self.model_step(batch)
        for name, (loss, scores, predictions, targets) in outputs.items():
            self.val_loss(loss)
            self.val_threshold_metrics[name].update(predictions, targets)
            self.val_ranking_metrics[name].update(scores, targets)

    def _reset_validation_metrics(self) -> None:
        """Clear validation metric state for all configured datasets."""
        self.val_loss.reset()
        for name in self.dataset_names:
            self.val_threshold_metrics[name].reset()
            self.val_ranking_metrics[name].reset()

    def on_validation_epoch_end(self) -> None:
        """Log per-dataset validation metrics and retain each best classifier head."""
        trainer = getattr(self, "_trainer", None)
        if trainer is not None and trainer.sanity_checking:
            self._reset_validation_metrics()
            return

        for name in self.dataset_names:
            values = (
                self.val_threshold_metrics[name].compute()
                | self.val_ranking_metrics[name].compute()
            )
            macro_f1 = float(values[f"{name}/f1_macro"])
            self.log(f"classification/val/{name}/f1_macro", macro_f1, on_epoch=True)
            self.log_dict(
                {
                    f"classification/val/{name}/{key.removeprefix(f'{name}/')}": value
                    for key, value in values.items()
                },
                on_epoch=True,
            )
            if macro_f1 > self.best_val_macro_f1[name]:
                self.best_val_macro_f1[name] = macro_f1
                head_state = {
                    key: value.detach().cpu().clone()
                    for key, value in self.classifiers[name].state_dict().items()
                }
                self.best_classifier_states[name] = head_state
                if self.encoder_freeze:
                    self.best_model_states[name] = {
                        f"classifier.{key}": value for key, value in head_state.items()
                    }
                else:
                    self.best_model_states[name] = {
                        **{
                            f"encoder.{key}": value.detach().cpu().clone()
                            for key, value in self.encoder.state_dict().items()
                        },
                        **{f"classifier.{key}": value for key, value in head_state.items()},
                    }
        self._reset_validation_metrics()

    def on_test_start(self) -> None:
        """Reset test metrics and per-dataset prediction buffers."""
        self.test_loss.reset()
        for name in self.dataset_names:
            self.test_threshold_metrics[name].reset()
            self.test_ranking_metrics[name].reset()
            self._test_prediction_scores[name] = []
            self._test_prediction_targets[name] = []

    def test_step(self, batch: BatchType, _: int) -> None:
        """Evaluate every dataset subset with its own best classifier head."""
        outputs = self.model_step(batch, use_best_classifier=True)
        for name, (loss, scores, predictions, targets) in outputs.items():
            self.test_loss(loss)
            self.test_threshold_metrics[name].update(predictions, targets)
            self.test_ranking_metrics[name].update(scores, targets)
            self._test_prediction_scores[name].append(scores.detach().cpu())
            self._test_prediction_targets[name].append(targets.detach().cpu())

    def on_test_epoch_end(self) -> None:
        """Log dataset-specific test metrics."""
        for name in self.dataset_names:
            values = (
                self.test_threshold_metrics[name].compute()
                | self.test_ranking_metrics[name].compute()
            )
            self.log_dict(
                {
                    f"classification/test/{name}/{key.removeprefix(f'{name}/')}": value
                    for key, value in values.items()
                },
                on_epoch=True,
            )
            self.test_threshold_metrics[name].reset()
            self.test_ranking_metrics[name].reset()
        self.test_loss.reset()

    def on_fit_start(self) -> None:
        """Load the optional encoder checkpoint and apply freeze policy."""
        self._configure_stage_metric_axes()
        self._initialize_encoder(
            "encoder_freeze=True requires pretrained_encoder_path or a pretrained encoder."
        )

    def _iter_artifact_experiments(self) -> list[Any]:
        """Return loggers that support prediction artifact uploads."""
        if self.trainer is None:
            return []
        return [
            experiment
            for logger in getattr(self.trainer, "loggers", [])
            if (experiment := getattr(logger, "experiment", None)) is not None
            and callable(getattr(experiment, "log_artifact", None))
        ]

    def _classification_test_prediction_dir(self) -> Path | None:
        """Create the local prediction artifact directory when artifact logging is enabled."""
        if not self._iter_artifact_experiments() or self.trainer is None:
            return None
        root_dir = getattr(self.trainer, "default_root_dir", ".")
        directory = Path(str(root_dir)) / "artifacts" / "multi_dataset_test_predictions"
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    def _log_test_prediction_artifact(
        self,
        artifact_path: Path,
        payload: dict[str, dict[str, torch.Tensor]],
    ) -> None:
        """Upload one artifact containing scores, targets, and dataset provenance."""
        import wandb

        num_examples = {name: int(values["scores"].shape[0]) for name, values in payload.items()}
        for experiment in self._iter_artifact_experiments():
            run_id = getattr(experiment, "id", None)
            artifact_name = (
                f"{run_id}-multi-dataset-test-predictions"
                if isinstance(run_id, str) and run_id
                else "multi-dataset-test-predictions"
            )
            artifact = wandb.Artifact(
                name=artifact_name,
                type="multi_dataset_test_predictions",
                description=(
                    "Dataset-specific sigmoid scores and targets with explicit dataset provenance."
                ),
                metadata={
                    "stage": "classification/test",
                    "format": "torch.save",
                    "datasets": list(payload),
                    "num_examples": num_examples,
                },
            )
            artifact.add_file(str(artifact_path), name=artifact_path.name)
            experiment.log_artifact(artifact)

    def on_test_end(self) -> None:
        """Persist dataset-specific test predictions as a W&B artifact when available."""
        artifact_dir = self._classification_test_prediction_dir()
        if artifact_dir is None or self.trainer is None:
            return
        local_payload = {
            name: {
                "scores": torch.cat(self._test_prediction_scores[name], dim=0),
                "targets": torch.cat(self._test_prediction_targets[name], dim=0),
            }
            for name in self.dataset_names
            if self._test_prediction_scores[name]
        }
        if not local_payload:
            return
        rank = int(getattr(self.trainer, "global_rank", 0))
        world_size = int(getattr(self.trainer, "world_size", 1))
        shard_path = artifact_dir / f"multi_dataset_test_predictions.rank{rank}.pt"
        torch.save(local_payload, shard_path)
        barrier = getattr(getattr(self.trainer, "strategy", None), "barrier", None)
        if callable(barrier):
            barrier()
        if rank != 0:
            return
        merged: dict[str, dict[str, list[torch.Tensor]]] = {
            name: {"scores": [], "targets": []} for name in self.dataset_names
        }
        for shard_rank in range(world_size):
            candidate = artifact_dir / f"multi_dataset_test_predictions.rank{shard_rank}.pt"
            if not candidate.exists():
                continue
            shard = torch.load(candidate, map_location="cpu", weights_only=False)
            for name, values in cast(dict[str, dict[str, torch.Tensor]], shard).items():
                merged[name]["scores"].append(values["scores"])
                merged[name]["targets"].append(values["targets"])
        payload = {
            name: {
                "scores": torch.cat(values["scores"], dim=0),
                "targets": torch.cat(values["targets"], dim=0),
            }
            for name, values in merged.items()
            if values["scores"]
        }
        artifact_path = artifact_dir / "multi_dataset_test_predictions.pt"
        torch.save(payload, artifact_path)
        self._log_test_prediction_artifact(artifact_path, payload)
        for shard_rank in range(world_size):
            candidate = artifact_dir / f"multi_dataset_test_predictions.rank{shard_rank}.pt"
            if candidate.exists():
                candidate.unlink()

    def configure_optimizers(self) -> Any:
        """Configure the optimizer and optional scheduler."""
        hparams = cast(Any, self.hparams)
        parameter_groups: list[dict[str, Any]] = []
        if not self.encoder_freeze:
            encoder_parameters = [
                parameter for parameter in self.encoder.parameters() if parameter.requires_grad
            ]
            if encoder_parameters:
                parameter_groups.append(
                    {"params": encoder_parameters, "lr": float(hparams.optimizer.lr)}
                )
        for name in self.dataset_names:
            parameter_groups.append(
                {
                    "params": [
                        parameter
                        for parameter in self.classifiers[name].parameters()
                        if parameter.requires_grad
                    ],
                    "lr": self.classifier_lr_by_dataset[name],
                }
            )
        optimizer = hparams.optimizer(params=parameter_groups)
        if hparams.scheduler is None:
            return {"optimizer": optimizer}
        return {
            "optimizer": optimizer,
            "lr_scheduler": {
                "scheduler": hparams.scheduler(optimizer=optimizer),
                "monitor": "classification/val/macro_f1",
                "interval": "epoch",
                "frequency": 1,
            },
        }
