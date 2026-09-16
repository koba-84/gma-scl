import sys
import types
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import pytest
import torch

from src.models.multi_dataset_finetune_module import MultiDatasetFinetuneLitModule


class _FeatureEncoder(torch.nn.Module):
    hidden_size = 4
    load_pretrained_weights = True

    def forward(self, inputs: dict[str, torch.Tensor]) -> torch.Tensor:
        return inputs["input_ids"].float()


class _ArtifactStub:
    def __init__(
        self, name: str, type: str, description: str, metadata: dict[str, object]
    ) -> None:
        self.name = name
        self.type = type
        self.description = description
        self.metadata = metadata
        self.files: list[tuple[str, str | None]] = []

    def add_file(self, path: str, name: str | None = None) -> None:
        self.files.append((path, name))


class _ExperimentStub:
    id = "run-multi"

    def __init__(self) -> None:
        self.artifacts: list[_ArtifactStub] = []

    def log_artifact(self, artifact: _ArtifactStub) -> None:
        self.artifacts.append(artifact)


class _StrategyStub:
    def barrier(self) -> None:
        return None


def test_multi_dataset_finetune_routes_mixed_batch_to_local_heads() -> None:
    module = MultiDatasetFinetuneLitModule(
        encoder=_FeatureEncoder(),
        optimizer=torch.optim.Adam,
        scheduler=None,
        dataset_names=["a", "b"],
        num_classes_by_dataset={"a": 2, "b": 2},
        label_offsets={"a": 0, "b": 2},
        classifier_lr_by_dataset={"a": 5.0e-4, "b": 5.0e-4},
        criterion=torch.nn.BCEWithLogitsLoss(),
    )
    inputs = {
        "input_ids": torch.randn(3, 4),
        "attention_mask": torch.ones(3, 4),
        "dataset_id": torch.tensor([0, 1, 0]),
    }
    labels = torch.tensor([[1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 0.0]])

    outputs = module.model_step((inputs, labels))

    assert set(outputs) == {"a", "b"}
    assert outputs["a"][1].shape == (2, 2)
    assert outputs["b"][1].shape == (1, 2)


def test_multi_dataset_finetune_uses_dataset_specific_classifier_lrs() -> None:
    module = MultiDatasetFinetuneLitModule(
        encoder=_FeatureEncoder(),
        optimizer=torch.optim.Adam,
        scheduler=None,
        dataset_names=["a", "b"],
        num_classes_by_dataset={"a": 2, "b": 2},
        label_offsets={"a": 0, "b": 2},
        classifier_lr_by_dataset={"a": 1.0e-3, "b": 2.0e-3},
        criterion=torch.nn.BCEWithLogitsLoss(),
    )

    configured = module.configure_optimizers()
    optimizer = configured["optimizer"]

    assert [group["lr"] for group in optimizer.param_groups] == [1.0e-3, 2.0e-3]


@pytest.mark.parametrize(
    "rates",
    [
        {"a": 1.0e-3},
        {"a": 0.0, "b": 1.0e-3},
        {"a": float("nan"), "b": 1.0e-3},
    ],
)
def test_multi_dataset_finetune_rejects_invalid_classifier_lrs(
    rates: dict[str, float],
) -> None:
    with pytest.raises(ValueError):
        MultiDatasetFinetuneLitModule(
            encoder=_FeatureEncoder(),
            optimizer=torch.optim.Adam,
            scheduler=None,
            dataset_names=["a", "b"],
            num_classes_by_dataset={"a": 2, "b": 2},
            label_offsets={"a": 0, "b": 2},
            classifier_lr_by_dataset=rates,
            criterion=torch.nn.BCEWithLogitsLoss(),
        )


def test_multi_dataset_finetune_selects_each_head_by_its_own_macro_f1() -> None:
    module = MultiDatasetFinetuneLitModule(
        encoder=_FeatureEncoder(),
        optimizer=torch.optim.Adam,
        scheduler=None,
        dataset_names=["a"],
        num_classes_by_dataset={"a": 2},
        label_offsets={"a": 0},
        classifier_lr_by_dataset={"a": 5.0e-4},
        criterion=torch.nn.BCEWithLogitsLoss(),
    )
    module.best_val_macro_f1["a"] = 0.5
    module.classifiers["a"].weight.data.fill_(2.0)
    module.classifiers["a"].bias.data.fill_(3.0)
    inputs = {
        "input_ids": torch.randn(2, 4),
        "attention_mask": torch.ones(2, 4),
        "dataset_id": torch.tensor([0, 0]),
    }
    module.validation_step(
        (
            inputs,
            torch.tensor([[1.0, 0.0], [0.0, 1.0]]),
        ),
        0,
    )
    module.on_validation_epoch_end()

    assert module.best_val_macro_f1["a"] >= 0.0


def test_multi_dataset_finetune_persists_dataset_provenance_artifact(
    tmp_path: Path, monkeypatch
) -> None:
    experiment = _ExperimentStub()
    trainer = SimpleNamespace(
        loggers=[SimpleNamespace(experiment=experiment)],
        default_root_dir=str(tmp_path),
        global_rank=0,
        world_size=1,
        strategy=_StrategyStub(),
    )
    monkeypatch.setitem(sys.modules, "wandb", types.SimpleNamespace(Artifact=_ArtifactStub))

    module = MultiDatasetFinetuneLitModule(
        encoder=_FeatureEncoder(),
        optimizer=torch.optim.Adam,
        scheduler=None,
        dataset_names=["a", "b"],
        num_classes_by_dataset={"a": 2, "b": 2},
        label_offsets={"a": 0, "b": 2},
        classifier_lr_by_dataset={"a": 5.0e-4, "b": 5.0e-4},
        criterion=torch.nn.BCEWithLogitsLoss(),
    )
    cast(Any, module).trainer = trainer
    inputs = {
        "input_ids": torch.randn(2, 4),
        "attention_mask": torch.ones(2, 4),
        "dataset_id": torch.tensor([0, 1]),
    }
    labels = torch.tensor([[1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]])

    module.on_test_start()
    module.test_step((inputs, labels), 0)
    module.on_test_end()

    artifact_path = tmp_path / "artifacts" / "multi_dataset_test_predictions"
    payload = torch.load(
        artifact_path / "multi_dataset_test_predictions.pt",
        map_location="cpu",
        weights_only=False,
    )
    assert set(payload) == {"a", "b"}
    assert payload["a"]["scores"].shape == (1, 2)
    assert payload["b"]["targets"].shape == (1, 2)
    assert len(experiment.artifacts) == 1
    assert experiment.artifacts[0].metadata["datasets"] == ["a", "b"]
