from collections.abc import Callable
from typing import Any, cast

import torch
import torch.nn.functional as functional
from lightning import LightningModule
from torch.nn.init import xavier_uniform_
from torch.optim.lr_scheduler import LRScheduler
from torchmetrics import MeanMetric

from src.data.components.gcbs import compute_gcbs_permutation
from src.models.components.encoder_lifecycle import EncoderLifecycleMixin
from src.models.loss.msc import MSC

BatchInput = dict[str, torch.Tensor]
BatchType = tuple[BatchInput, torch.Tensor]
MetricAxisDefinition = tuple[str, dict[str, object]]


def _contrastive_metric_axis_definitions() -> tuple[MetricAxisDefinition, ...]:
    return (
        ("contrastive/epoch", {}),
        (
            "contrastive/train/loss",
            {"step_metric": "contrastive/epoch", "step_sync": True},
        ),
        (
            "contrastive/val/loss",
            {"step_metric": "contrastive/epoch", "step_sync": True},
        ),
    )


class ContrastiveLitModule(EncoderLifecycleMixin, LightningModule):
    """LightningModule for supervised contrastive pretraining."""

    def __init__(
        self,
        encoder: torch.nn.Module,
        projection_head: torch.nn.Module,
        optimizer: Callable[..., torch.optim.Optimizer],
        scheduler: Callable[..., LRScheduler] | None,
        loss_fn: Callable[..., torch.Tensor] | None = None,
        warmup_ratio: float = 0.0,
        warmup_start_factor: float = 0.1,
        compile: bool = False,
    ) -> None:
        super().__init__()
        self.save_hyperparameters(logger=False, ignore=["encoder", "projection_head", "loss_fn"])

        self.encoder = encoder
        self.projection_head = projection_head
        self.loss_fn = loss_fn
        self.register_parameter("prototype", None)

        self.train_loss = MeanMetric()
        self.val_loss = MeanMetric()

    def forward(self, x: BatchInput) -> torch.Tensor:
        """Encode tokenized batch inputs."""
        return self.encoder(x)

    def on_train_start(self) -> None:
        """Reset epoch metrics at training start."""
        self.train_loss.reset()
        self.val_loss.reset()

    def on_fit_start(self) -> None:
        """Configure metrics and initialize dynamic samplers."""
        self._configure_stage_metric_axes()
        self._refresh_dynamic_sampler(force=False)

    def _configure_stage_metric_axes(self) -> None:
        if self.trainer is None:
            return
        for logger in self.trainer.loggers:
            experiment = getattr(logger, "experiment", None)
            define_metric = getattr(experiment, "define_metric", None)
            if callable(define_metric):
                for metric_name, metric_kwargs in _contrastive_metric_axis_definitions():
                    define_metric(metric_name, **metric_kwargs)

    def _compute_gcbs_embeddings(self, refresh_batches: list[BatchInput]) -> torch.Tensor:
        was_training = self.training
        self.eval()
        outputs: list[torch.Tensor] = []
        with torch.no_grad():
            for batch_inputs in refresh_batches:
                reps = self._project(batch_inputs)
                outputs.append(reps.detach().cpu())
        if was_training:
            self.train()
        if not outputs:
            return torch.empty((0, 0))
        return torch.cat(outputs, dim=0)

    def _project(self, x: BatchInput) -> torch.Tensor:
        h = self.encoder(x)
        z = self.projection_head(h)
        return z

    def _use_msc_prototype(self) -> bool:
        return isinstance(self.loss_fn, MSC)

    def _init_learnable_prototype(self) -> None:
        if not self._use_msc_prototype() or self.prototype is not None:
            return
        if self.trainer is None:
            raise RuntimeError("datamodule is required to initialize learnable prototypes.")
        datamodule = getattr(self.trainer, "datamodule", None)
        if datamodule is None:
            raise RuntimeError("datamodule is required to initialize learnable prototypes.")
        num_classes = int(getattr(datamodule, "num_classes", 0))
        if num_classes <= 0:
            raise RuntimeError("num_classes must be > 0 to initialize learnable prototypes.")
        if not hasattr(self.projection_head, "model"):
            raise RuntimeError("Unable to infer projection output dimension from projection_head.")
        layers = getattr(self.projection_head, "model")
        if len(layers) == 0 or not hasattr(layers[-1], "out_features"):
            raise RuntimeError("Unable to infer projection output dimension from projection_head.")
        out_dim = int(layers[-1].out_features)
        proto = torch.nn.Parameter(torch.empty(num_classes, out_dim))
        xavier_uniform_(proto)
        self.register_parameter("prototype", proto)

    def model_step(self, batch: BatchType) -> torch.Tensor:
        """Compute contrastive loss for one batch."""
        x, labels = batch
        z = self._project(x)
        loss_fn = self.loss_fn
        if loss_fn is None:
            raise RuntimeError("loss_fn is required. Set model.loss_fn in the config.")
        if self._use_msc_prototype():
            prototype = cast(torch.nn.Parameter | None, self.prototype)
            if prototype is None:
                raise RuntimeError("prototype is not initialized.")
            if int(prototype.shape[0]) != labels.size(1):
                raise RuntimeError(
                    f"prototype rows ({int(prototype.shape[0])}) must match label dim ({labels.size(1)})."
                )
            normalized_prototype = functional.normalize(
                prototype.to(device=z.device, dtype=z.dtype),
                dim=1,
            )
            return cast(MSC, loss_fn)(z, labels, prototype=normalized_prototype)
        return loss_fn(z, labels)

    def training_step(self, batch: BatchType, _: int) -> torch.Tensor:
        """Run one training step and log train loss."""
        loss = self.model_step(batch)
        self.train_loss(loss)
        batch_size = int(batch[1].size(0))
        self.log(
            "contrastive/epoch",
            float(self.current_epoch),
            on_step=False,
            on_epoch=True,
            batch_size=batch_size,
        )
        self.log(
            "contrastive/train/loss",
            self.train_loss,
            on_step=False,
            on_epoch=True,
            prog_bar=True,
        )
        return loss

    def validation_step(self, batch: BatchType, _: int) -> None:
        """Run one validation step and log validation loss."""
        loss = self.model_step(batch)
        self.val_loss(loss)
        batch_size = int(batch[1].size(0))
        self.log(
            "contrastive/epoch",
            float(self.current_epoch),
            on_step=False,
            on_epoch=True,
            batch_size=batch_size,
        )
        self.log(
            "contrastive/val/loss",
            self.val_loss,
            on_step=False,
            on_epoch=True,
            prog_bar=True,
        )

    def _refresh_dynamic_sampler(self, force: bool) -> None:
        if self.trainer is None:
            return
        datamodule = getattr(self.trainer, "datamodule", None)
        if datamodule is None or not getattr(datamodule, "get_sampler_type", None):
            return
        sampler_type = datamodule.get_sampler_type()
        if sampler_type not in {"gcbs", "dpp"}:
            return
        if sampler_type == "dpp" and not force:
            batch_sampler = getattr(datamodule, "train_batch_sampler", None)
            if (
                batch_sampler is not None
                and getattr(batch_sampler, "is_initialized", lambda: False)()
            ):
                return

        cfg = datamodule.get_sampler_config(sampler_type)

        refresh_batches = datamodule.iter_refresh_batches()
        embeddings = self._compute_gcbs_embeddings(refresh_batches)
        if sampler_type == "gcbs":
            quantile = float(cfg.get("quantile", 0.999))
            chunk_size = int(cfg.get("chunk_size", 10))
            chunk_size = max(chunk_size, 1)
            perm = compute_gcbs_permutation(
                embeddings,
                quantile=quantile,
                chunk_size=chunk_size,
            )
            datamodule.set_gcbs_indices(perm)
        else:
            datamodule.set_dpp_embeddings(embeddings)

    def on_train_epoch_start(self) -> None:
        """Refresh sampler state before each epoch."""
        self._refresh_dynamic_sampler(force=True)

    def setup(self, stage: str) -> None:
        """Initialize stage-specific runtime state."""
        if stage == "fit":
            self._init_learnable_prototype()
        super().setup(stage)

    def _compile_additional_modules(self) -> None:
        """Compile the projection head after the shared encoder."""
        self.projection_head = cast(torch.nn.Module, torch.compile(self.projection_head))

    def configure_optimizers(self) -> Any:
        """Configure optimizer and optional scheduler."""
        hparams = cast(Any, self.hparams)
        optimizer = hparams.optimizer(params=self.parameters())
        if hparams.scheduler is not None:
            warmup_ratio = float(getattr(hparams, "warmup_ratio", 0.0) or 0.0)
            if warmup_ratio > 0.0:
                trainer = self.trainer
                if trainer is None or trainer.max_epochs is None:
                    raise RuntimeError("trainer.max_epochs is required for warmup scheduling.")
                max_epochs = int(trainer.max_epochs)
                warmup_epochs = max(1, int(max_epochs * warmup_ratio))
                warmup_start_factor = float(getattr(hparams, "warmup_start_factor", 0.1) or 0.1)
                warmup = torch.optim.lr_scheduler.LinearLR(
                    optimizer,
                    start_factor=warmup_start_factor,
                    end_factor=1.0,
                    total_iters=warmup_epochs,
                )
                remaining_epochs = max(1, max_epochs - warmup_epochs)
                scheduler_cfg = hparams.scheduler
                if (
                    getattr(scheduler_cfg, "func", None)
                    is torch.optim.lr_scheduler.CosineAnnealingLR
                ):
                    eta_min = getattr(scheduler_cfg, "keywords", {}).get("eta_min", 0.0)
                    cosine = torch.optim.lr_scheduler.CosineAnnealingLR(
                        optimizer,
                        T_max=remaining_epochs,
                        eta_min=eta_min,
                    )
                else:
                    cosine = scheduler_cfg(optimizer=optimizer)
                scheduler = torch.optim.lr_scheduler.SequentialLR(
                    optimizer,
                    schedulers=[warmup, cosine],
                    milestones=[warmup_epochs],
                )
            else:
                scheduler = hparams.scheduler(optimizer=optimizer)
            return {
                "optimizer": optimizer,
                "lr_scheduler": {
                    "scheduler": scheduler,
                    "monitor": "contrastive/val/loss",
                    "interval": "epoch",
                    "frequency": 1,
                },
            }
        return {"optimizer": optimizer}


if __name__ == "__main__":
    _ = ContrastiveLitModule(
        encoder=torch.nn.Identity(),
        projection_head=torch.nn.Identity(),
        optimizer=torch.optim.Adam,
        scheduler=None,
        loss_fn=lambda z, labels: z.sum() * 0.0 + labels.sum() * 0.0,
    )
