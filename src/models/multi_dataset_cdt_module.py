from __future__ import annotations

from collections.abc import Callable
from typing import Any, cast

import torch
from lightning import LightningModule
from torch.optim.lr_scheduler import LRScheduler
from torchmetrics import MeanMetric

from src.models.components.encoder_lifecycle import EncoderLifecycleMixin
from src.models.loss.multi_dataset_cdt import MultiDatasetCDT

BatchInput = dict[str, torch.Tensor]
BatchType = tuple[BatchInput, torch.Tensor]
OptimizerFactory = Callable[..., torch.optim.Optimizer]
SchedulerFactory = Callable[..., LRScheduler]


class MultiDatasetCDTLitModule(EncoderLifecycleMixin, LightningModule):
    """Shared encoder with epoch-refreshed CDT covariances."""

    def __init__(
        self,
        encoder: torch.nn.Module,
        projection_head: torch.nn.Module,
        optimizer: OptimizerFactory,
        scheduler: SchedulerFactory | None,
        loss_fn: MultiDatasetCDT,
        compile: bool = False,
    ) -> None:
        super().__init__()
        if not isinstance(loss_fn, MultiDatasetCDT):
            raise TypeError("MultiDatasetCDTLitModule requires MultiDatasetCDT.")
        projection_dim = int(getattr(projection_head, "out_dim", loss_fn.embedding_dim))
        if projection_dim != loss_fn.embedding_dim:
            raise ValueError(
                "projection_head output dimension must match loss_fn.embedding_dim: "
                f"{projection_dim} != {loss_fn.embedding_dim}"
            )
        self.save_hyperparameters(logger=False, ignore=["encoder", "projection_head", "loss_fn"])
        self.encoder = encoder
        self.projection_head = projection_head
        self.loss_fn = loss_fn
        self.train_loss = MeanMetric()
        self.val_loss = MeanMetric()
        self._covariance_epoch: int | None = None

    def forward(self, inputs: BatchInput) -> torch.Tensor:
        """Encode and project a mixed batch."""
        return self._project(inputs)

    def _project(self, inputs: BatchInput) -> torch.Tensor:
        return self.projection_head(self.encoder(inputs))

    def model_step(self, batch: BatchType) -> torch.Tensor:
        """Compute CDT against the existing semantic label graph."""
        inputs, labels = batch
        dataset_ids = inputs.get("dataset_id")
        if dataset_ids is None:
            raise ValueError("CDT batches must contain dataset_id.")
        return self.loss_fn(self._project(inputs), labels, dataset_ids)

    def _refresh_domain_covariances(self) -> None:
        """Encode the full training split and refresh detached domain covariances."""
        trainer = self.trainer
        datamodule = getattr(trainer, "datamodule", None)
        covariance_dataloader = getattr(datamodule, "covariance_dataloader", None)
        if not callable(covariance_dataloader):
            raise RuntimeError("CDT requires a datamodule with covariance_dataloader().")

        embeddings_by_domain: list[list[torch.Tensor]] = [
            [] for _ in range(self.loss_fn.num_domains)
        ]
        was_training = self.training
        self.eval()
        try:
            with torch.no_grad():
                for inputs, _labels in covariance_dataloader():
                    device_inputs = {
                        name: value.to(device=self.device) for name, value in inputs.items()
                    }
                    projected = self._project(device_inputs).to(dtype=torch.float32)
                    dataset_ids = device_inputs.get("dataset_id")
                    if dataset_ids is None:
                        raise ValueError("CDT covariance batches must contain dataset_id.")
                    for domain_id in range(self.loss_fn.num_domains):
                        mask = dataset_ids == domain_id
                        if torch.any(mask):
                            embeddings_by_domain[domain_id].append(projected[mask].detach().cpu())
        finally:
            self.train(was_training)

        covariances: list[torch.Tensor] = []
        for domain_id, chunks in enumerate(embeddings_by_domain):
            if not chunks:
                raise RuntimeError(
                    f"CDT covariance refresh found no training embeddings for domain {domain_id}."
                )
            embeddings = torch.cat(chunks, dim=0).to(dtype=torch.float64)
            sample_count = embeddings.size(0)
            if sample_count < 2:
                raise RuntimeError(
                    "CDT covariance refresh requires at least two training embeddings for "
                    f"domain {domain_id}; found {sample_count}."
                )
            centered = embeddings - embeddings.mean(dim=0, keepdim=True)
            covariance = centered.T @ centered / (sample_count - 1)
            covariances.append(covariance.to(dtype=torch.float32))

        self.loss_fn.set_domain_covariances(torch.stack(covariances).to(device=self.device))
        self._covariance_epoch = int(self.current_epoch)

    def on_fit_start(self) -> None:
        """Initialize covariance state before Lightning's sanity validation."""
        if self._covariance_epoch != int(self.current_epoch):
            self._refresh_domain_covariances()

    def on_train_epoch_start(self) -> None:
        """Refresh covariances once before optimization for each epoch."""
        if self._covariance_epoch != int(self.current_epoch):
            self._refresh_domain_covariances()

    def on_train_start(self) -> None:
        """Reset train and validation loss metrics."""
        self.train_loss.reset()
        self.val_loss.reset()

    def training_step(self, batch: BatchType, _: int) -> torch.Tensor:
        """Run one mixed-dataset CDT training step."""
        loss = self.model_step(batch)
        self.train_loss(loss)
        self.log("contrastive/epoch", float(self.current_epoch), on_step=False, on_epoch=True)
        self.log("contrastive/train/loss", self.train_loss, on_step=False, on_epoch=True)
        return loss

    def validation_step(self, batch: BatchType, _: int) -> None:
        """Evaluate CDT with the covariance state from the latest training refresh."""
        loss = self.model_step(batch)
        self.val_loss(loss)
        self.log("contrastive/epoch", float(self.current_epoch), on_step=False, on_epoch=True)
        self.log("contrastive/val/loss", self.val_loss, on_step=False, on_epoch=True)

    def _compile_additional_modules(self) -> None:
        """Compile the projection head after the shared encoder."""
        self.projection_head = cast(torch.nn.Module, torch.compile(self.projection_head))

    def configure_optimizers(self) -> Any:
        """Configure the existing single encoder/projection optimizer contract."""
        hparams = cast(Any, self.hparams)
        optimizer = hparams.optimizer(params=self.parameters())
        if hparams.scheduler is None:
            return {"optimizer": optimizer}
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


__all__ = ["MultiDatasetCDTLitModule"]
