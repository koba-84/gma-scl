from __future__ import annotations

from collections.abc import Callable
from typing import Any, cast

import torch
from lightning import LightningModule
from torch.optim.lr_scheduler import LRScheduler
from torchmetrics import MeanMetric

from src.models.components.encoder_lifecycle import EncoderLifecycleMixin
from src.models.loss.multi_dataset_mxclr import MultiDatasetMXCLR

BatchInput = dict[str, torch.Tensor]
BatchType = tuple[BatchInput, torch.Tensor]
OptimizerFactory = Callable[..., torch.optim.Optimizer]
SchedulerFactory = Callable[..., LRScheduler]


class MultiDatasetContrastiveLitModule(EncoderLifecycleMixin, LightningModule):
    """Shared encoder and label-embedding-only MXCLR for mixed datasets."""

    def __init__(
        self,
        encoder: torch.nn.Module,
        projection_head: torch.nn.Module,
        optimizer: OptimizerFactory,
        scheduler: SchedulerFactory | None,
        loss_fn: torch.nn.Module,
        compile: bool = False,
    ) -> None:
        super().__init__()
        if not isinstance(loss_fn, MultiDatasetMXCLR):
            raise TypeError(
                "MultiDatasetContrastiveLitModule requires MultiDatasetMXCLR; "
                "IDF/NPMI and ranking losses are not supported."
            )
        self.save_hyperparameters(logger=False, ignore=["encoder", "projection_head", "loss_fn"])
        self.encoder = encoder
        self.projection_head = projection_head
        self.loss_fn = loss_fn
        self.train_loss = MeanMetric()
        self.val_loss = MeanMetric()

    def forward(self, inputs: BatchInput) -> torch.Tensor:
        """Encode a batch with the shared encoder."""
        return self.encoder(inputs)

    def _project(self, inputs: BatchInput) -> torch.Tensor:
        return self.projection_head(self.encoder(inputs))

    def model_step(self, batch: BatchType) -> torch.Tensor:
        """Compute label-embedding-only MXCLR for a mixed batch."""
        inputs, labels = batch
        return self.loss_fn(self._project(inputs), labels)

    def on_train_start(self) -> None:
        """Reset train and validation loss metrics."""
        self.train_loss.reset()
        self.val_loss.reset()

    def training_step(self, batch: BatchType, _: int) -> torch.Tensor:
        """Run one mixed-dataset contrastive training step."""
        loss = self.model_step(batch)
        self.train_loss(loss)
        self.log("contrastive/epoch", float(self.current_epoch), on_step=False, on_epoch=True)
        self.log("contrastive/train/loss", self.train_loss, on_step=False, on_epoch=True)
        return loss

    def validation_step(self, batch: BatchType, _: int) -> None:
        """Run one mixed-dataset contrastive validation step."""
        loss = self.model_step(batch)
        self.val_loss(loss)
        self.log("contrastive/epoch", float(self.current_epoch), on_step=False, on_epoch=True)
        self.log("contrastive/val/loss", self.val_loss, on_step=False, on_epoch=True)

    def _compile_additional_modules(self) -> None:
        """Compile the projection head after the shared encoder."""
        self.projection_head = cast(torch.nn.Module, torch.compile(self.projection_head))

    def configure_optimizers(self) -> Any:
        """Configure the optimizer and optional warmup/cosine scheduler."""
        hparams = cast(Any, self.hparams)
        optimizer = hparams.optimizer(params=self.parameters())
        if hparams.scheduler is None:
            return {"optimizer": optimizer}
        scheduler_cfg = hparams.scheduler
        scheduler = scheduler_cfg(optimizer=optimizer)
        return {
            "optimizer": optimizer,
            "lr_scheduler": {
                "scheduler": scheduler,
                "monitor": "contrastive/val/loss",
                "interval": "epoch",
                "frequency": 1,
            },
        }
