from __future__ import annotations

from types import SimpleNamespace
from typing import Any, cast

import torch

from src.models.finetune_module import FinetuneLitModule


class _EncoderStub(torch.nn.Module):
    hidden_size = 3

    def forward(self, inputs: dict[str, torch.Tensor]) -> torch.Tensor:
        return inputs["input_ids"]


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


def test_validation_epoch_end_logs_metric_collections() -> None:
    trainer = SimpleNamespace(
        loggers=[],
        default_root_dir=".",
        current_epoch=3,
        global_rank=0,
        world_size=1,
        strategy=_StrategyStub(),
    )
    log_calls: list[tuple[str, object]] = []
    log_dict_calls: list[dict[str, torch.Tensor]] = []

    module = _build_module()
    cast(Any, module).trainer = trainer
    cast(Any, module).log = lambda name, value, **kwargs: log_calls.append((name, value))
    cast(Any, module).log_dict = lambda payload, **kwargs: log_dict_calls.append(payload)

    module.validation_step(_build_batch(), 0)
    module.on_validation_epoch_end()

    assert ("classification/epoch", 3.0) in log_calls
    assert any(name == "classification/val/loss" for name, _ in log_calls)
    assert len(log_dict_calls) == 1
    assert set(log_dict_calls[0]) == {
        "classification/val/f1_macro",
        "classification/val/f1_micro",
        "classification/val/hamming_loss",
        "classification/val/map",
    }


def test_test_epoch_end_logs_metric_collections() -> None:
    trainer = SimpleNamespace(
        loggers=[],
        default_root_dir=".",
        current_epoch=4,
        global_rank=0,
        world_size=1,
        strategy=_StrategyStub(),
    )
    log_calls: list[tuple[str, object]] = []
    log_dict_calls: list[dict[str, torch.Tensor]] = []

    module = _build_module()
    cast(Any, module).trainer = trainer
    cast(Any, module).log = lambda name, value, **kwargs: log_calls.append((name, value))
    cast(Any, module).log_dict = lambda payload, **kwargs: log_dict_calls.append(payload)

    module.on_test_start()
    module.test_step(_build_batch(), 0)
    module.on_test_epoch_end()
    module.on_test_end()

    assert ("classification/epoch", 4.0) in log_calls
    assert len(log_dict_calls) == 1
    assert set(log_dict_calls[0]) == {
        "classification/test/f1_macro",
        "classification/test/f1_micro",
        "classification/test/hamming_loss",
        "classification/test/map",
    }
