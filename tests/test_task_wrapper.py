import sys
import types
from contextlib import nullcontext
from unittest.mock import Mock

import pytest
from omegaconf import OmegaConf

import src.utils.utils as utils_module
from src.utils.utils import task_wrapper


def _make_cfg():
    return OmegaConf.create({"paths": {"output_dir": "tmp/test-output"}})


def _install_mock_wandb(monkeypatch):
    finish = Mock()
    wandb_stub = types.SimpleNamespace(run=object(), finish=finish)
    monkeypatch.setattr(utils_module, "find_spec", lambda _: object())
    monkeypatch.setitem(sys.modules, "wandb", wandb_stub)
    return finish


@pytest.mark.parametrize(
    ("should_raise", "expected_exit_code", "expectation"),
    [
        pytest.param(False, 0, nullcontext(), id="success"),
        pytest.param(True, 1, pytest.raises(RuntimeError, match="boom"), id="failure"),
    ],
)
def test_task_wrapper_finishes_wandb_with_expected_exit_code(
    monkeypatch,
    should_raise: bool,
    expected_exit_code: int,
    expectation,
):
    finish = _install_mock_wandb(monkeypatch)

    @task_wrapper
    def _task(cfg):
        if should_raise:
            raise RuntimeError("boom")
        return {"ok": 1}, {"cfg": cfg}

    with expectation:
        _task(_make_cfg())

    finish.assert_called_once_with(exit_code=expected_exit_code)
