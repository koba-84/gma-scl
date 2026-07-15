from __future__ import annotations

import sys
import types
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import torch

from src.models.finetune_module import FinetuneLitModule


class _EncoderStub(torch.nn.Module):
    hidden_size = 3

    def forward(self, inputs: dict[str, torch.Tensor]) -> torch.Tensor:
        return inputs["input_ids"]


class _ArtifactStub:
    def __init__(
        self,
        name: str,
        type: str,
        description: str,
        metadata: dict[str, object],
    ) -> None:
        self.name = name
        self.type = type
        self.description = description
        self.metadata = metadata
        self.files: list[tuple[str, str | None]] = []

    def add_file(self, path: str, name: str | None = None) -> None:
        self.files.append((path, name))


class _ExperimentStub:
    def __init__(self) -> None:
        self.id = "run-123"
        self.artifacts: list[_ArtifactStub] = []

    def log_artifact(self, artifact: _ArtifactStub) -> None:
        self.artifacts.append(artifact)


class _StrategyStub:
    def barrier(self) -> None:
        return None


def _build_module() -> FinetuneLitModule:
    module = FinetuneLitModule(
        encoder=_EncoderStub(),
        optimizer=torch.optim.Adam,
        scheduler=None,
        num_classes=2,
        criterion=torch.nn.BCEWithLogitsLoss(),
        compile=False,
    )
    with torch.no_grad():
        module.classifier.weight.copy_(torch.tensor([[1.0, 0.0, 1.0], [0.0, 1.0, 0.0]]))
        module.classifier.bias.zero_()
    cast(Any, module).log = lambda *args, **kwargs: None
    return module


def _build_batch() -> tuple[dict[str, torch.Tensor], torch.Tensor]:
    return (
        {
            "input_ids": torch.tensor([[1.0, 0.0, 1.0], [0.0, 1.0, 0.0]], dtype=torch.float32),
            "attention_mask": torch.ones((2, 3), dtype=torch.float32),
            "empty_text_mask": torch.zeros(2, dtype=torch.bool),
        },
        torch.tensor([[1.0, 0.0], [0.0, 1.0]], dtype=torch.float32),
    )


def test_on_test_end_logs_prediction_artifact(tmp_path: Path, monkeypatch) -> None:
    experiment = _ExperimentStub()
    logger = SimpleNamespace(experiment=experiment)
    trainer = SimpleNamespace(
        loggers=[logger],
        default_root_dir=str(tmp_path),
        current_epoch=0,
        global_rank=0,
        world_size=1,
        strategy=_StrategyStub(),
    )
    monkeypatch.setitem(sys.modules, "wandb", types.SimpleNamespace(Artifact=_ArtifactStub))

    module = _build_module()
    cast(Any, module).trainer = trainer
    batch = _build_batch()

    module.on_test_start()
    module.test_step(batch, 0)
    module.on_test_end()

    artifact_path = tmp_path / "artifacts" / "classification_test_predictions"
    saved_payload = torch.load(
        artifact_path / "classification_test_predictions.pt",
        map_location="cpu",
        weights_only=False,
    )

    expected_scores = torch.sigmoid(torch.tensor([[2.0, 0.0], [0.0, 1.0]], dtype=torch.float32))
    expected_targets = batch[1].int()

    assert torch.allclose(saved_payload["scores"], expected_scores)
    assert torch.equal(saved_payload["targets"], expected_targets)
    assert len(experiment.artifacts) == 1
    artifact = experiment.artifacts[0]
    assert artifact.name == "run-123-classification-test-predictions"
    assert artifact.type == "classification_test_predictions"
    assert artifact.metadata == {
        "stage": "classification/test",
        "format": "torch.save",
        "num_examples": 2,
        "num_classes": 2,
    }
    assert artifact.files == [
        (
            str(artifact_path / "classification_test_predictions.pt"),
            "classification_test_predictions.pt",
        )
    ]


def test_on_test_end_skips_prediction_artifact_without_wandb_logger(tmp_path: Path) -> None:
    trainer = SimpleNamespace(
        loggers=[],
        default_root_dir=str(tmp_path),
        current_epoch=0,
        global_rank=0,
        world_size=1,
        strategy=_StrategyStub(),
    )

    module = _build_module()
    cast(Any, module).trainer = trainer
    batch = _build_batch()

    module.on_test_start()
    module.test_step(batch, 0)
    module.on_test_end()

    artifact_dir = tmp_path / "artifacts" / "classification_test_predictions"
    assert artifact_dir.exists() is False
