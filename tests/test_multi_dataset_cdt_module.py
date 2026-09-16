from typing import cast

import torch
from lightning import LightningDataModule, Trainer
from torch.utils.data import DataLoader, Dataset

from src.models.loss.multi_dataset_cdt import MultiDatasetCDT
from src.models.multi_dataset_cdt_module import MultiDatasetCDTLitModule


class _FeatureEncoder(torch.nn.Module):
    hidden_size = 2

    def __init__(self) -> None:
        super().__init__()
        self.layer = torch.nn.Linear(2, 2, bias=False)

    def forward(self, inputs: dict[str, torch.Tensor]) -> torch.Tensor:
        return self.layer(inputs["input_ids"].float())


class _SyntheticDataset(Dataset[tuple[dict[str, torch.Tensor], torch.Tensor]]):
    def __init__(self) -> None:
        self.rows = [
            (torch.tensor([1.0, 0.0]), torch.tensor([1.0, 0.0, 0.0]), 0),
            (torch.tensor([2.0, 0.0]), torch.tensor([0.0, 1.0, 0.0]), 0),
            (torch.tensor([0.0, 1.0]), torch.tensor([0.0, 0.0, 1.0]), 1),
            (torch.tensor([0.0, 2.0]), torch.tensor([1.0, 0.0, 0.0]), 1),
        ]

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, index: int) -> tuple[dict[str, torch.Tensor], torch.Tensor]:
        features, labels, dataset_id = self.rows[index]
        return {"input_ids": features, "dataset_id": torch.tensor(dataset_id)}, labels


class _SyntheticDataModule(LightningDataModule):
    def __init__(self) -> None:
        super().__init__()
        self.dataset = _SyntheticDataset()
        self.covariance_passes = 0

    def covariance_dataloader(self) -> DataLoader:
        self.covariance_passes += 1
        return DataLoader(self.dataset, batch_size=4, shuffle=False, drop_last=False)

    def train_dataloader(self) -> DataLoader:
        return DataLoader(self.dataset, batch_size=4, shuffle=False, drop_last=False)


def test_cdt_module_refreshes_covariance_before_training() -> None:
    loss = MultiDatasetCDT(num_domains=2, embedding_dim=2, label_embeddings=torch.eye(3))
    module = MultiDatasetCDTLitModule(
        encoder=_FeatureEncoder(),
        projection_head=torch.nn.Identity(),
        optimizer=torch.optim.Adam,
        scheduler=None,
        loss_fn=loss,
        compile=False,
    )
    datamodule = _SyntheticDataModule()
    trainer = Trainer(
        accelerator="cpu",
        devices=1,
        max_epochs=1,
        limit_train_batches=1,
        enable_checkpointing=False,
        enable_model_summary=False,
        logger=False,
    )

    trainer.fit(module, datamodule=datamodule)

    assert datamodule.covariance_passes == 1
    assert bool(cast(torch.Tensor, loss.covariance_ready).item())
    assert torch.isfinite(cast(torch.Tensor, loss.domain_covariances)).all()
