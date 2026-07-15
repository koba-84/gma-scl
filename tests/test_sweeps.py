from pathlib import Path

import pytest

from tests.support.run_if import run_if
from tests.support.run_sh_command import run_sh_command

startfile = "src/train.py"
overrides = ["logger=[]"]
pytestmark = [pytest.mark.integration, pytest.mark.slow]


@run_if(sh=True)
@pytest.mark.parametrize(
    ("case_name", "extra_args"),
    [
        pytest.param(
            "experiments",
            [
                "experiment=glob(*)",
                "++trainer.fast_dev_run=true",
            ],
            id="experiments",
        ),
        pytest.param(
            "hydra_sweep",
            [
                "contrastive=train",
                "contrastive.model.optimizer.lr=0.005,0.01",
                "++trainer.fast_dev_run=true",
            ],
            id="hydra_sweep",
        ),
        pytest.param(
            "hydra_sweep_ddp_sim",
            [
                "trainer=ddp_sim",
                "trainer.max_epochs=3",
                "+trainer.limit_train_batches=0.01",
                "+trainer.limit_val_batches=0.1",
                "+trainer.limit_test_batches=0.1",
                "contrastive=train",
                "contrastive.model.optimizer.lr=0.005,0.01,0.02",
            ],
            id="hydra_sweep_ddp_sim",
        ),
    ],
)
def test_sweeps(tmp_path: Path, case_name: str, extra_args: list[str]) -> None:
    """Test sweep entrypoints with case-specific multirun arguments."""
    command = [
        startfile,
        "-m",
        "hydra.sweep.dir=" + str(tmp_path / case_name),
        *extra_args,
    ] + overrides
    run_sh_command(command)
