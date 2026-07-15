from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest


class _CaptureLogger:
    def __init__(self) -> None:
        self.logged: dict[str, Any] | None = None

    def log_hyperparams(self, params: dict[str, Any]) -> None:
        self.logged = params


@pytest.fixture
def capture_logger() -> _CaptureLogger:
    return _CaptureLogger()


@pytest.fixture
def logging_runtime(capture_logger: _CaptureLogger) -> tuple[SimpleNamespace, SimpleNamespace]:
    trainer = SimpleNamespace(logger=True, loggers=[capture_logger])
    model = SimpleNamespace(parameters=lambda: [])
    return trainer, model
