from __future__ import annotations

from pathlib import Path

import pytest
import torch

from src.models.loss.mxclr import MXCLR
from tests.support.fixtures.datasets import write_label_descriptions_json


@pytest.fixture(scope="function")
def stub_mxclr_dependencies(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "src.models.loss.mxclr.MXCLR._encode_descriptions_with_sbert",
        staticmethod(
            lambda descriptions, model_name, max_length: torch.zeros((len(descriptions), 2))
        ),
    )
    monkeypatch.setattr(
        "src.models.loss.mxclr.compute_npmi",
        lambda data_dir, dataset_name: torch.eye(54, dtype=torch.float32),
    )
    monkeypatch.setattr(
        "src.models.loss.mxclr.compute_frequency",
        lambda data_dir, dataset_name: torch.ones(54, dtype=torch.float32),
    )
    monkeypatch.setattr(
        "src.models.loss.mxclr.compute_idf",
        lambda data_dir, dataset_name: torch.ones(54, dtype=torch.float32),
    )


@pytest.fixture(scope="function")
def mxclr_dataset_factory(tmp_path: Path):
    def _build(
        *,
        dataset_name: str = "mxclr_test_dataset",
        descriptions: list[str] | None = None,
        train_rows: list[str] | None = None,
    ) -> tuple[Path, str, Path]:
        data_root = tmp_path / "data"
        resolved_descriptions = descriptions or ["alpha topic", "beta topic", "gamma topic"]
        dataset_dir = write_label_descriptions_json(
            data_root=data_root,
            dataset_name=dataset_name,
            descriptions=resolved_descriptions,
        )
        resolved_train_rows = train_rows
        if resolved_train_rows is None:
            resolved_train_rows = [
                "doc1,1,0,1\n",
                "doc2,1,0,0\n",
                "doc3,0,1,0\n",
                "doc4,0,1,1\n",
            ]

        if resolved_train_rows is not None:
            label_columns = [
                f"label_{chr(ord('a') + index)}" for index in range(len(resolved_descriptions))
            ]
            (dataset_dir / "train.csv").write_text(
                ",".join(["text", *label_columns]) + "\n" + "".join(resolved_train_rows),
                encoding="utf-8",
            )
        return data_root, dataset_name, dataset_dir

    return _build


@pytest.fixture(scope="function")
def stub_mxclr_encoder(monkeypatch: pytest.MonkeyPatch):
    base_embeddings = torch.tensor(
        [
            [1.0, 0.0],
            [0.8, 0.2],
            [0.0, 1.0],
            [0.2, 0.8],
        ],
        dtype=torch.float32,
    )

    def _stub(embeddings: torch.Tensor | None = None) -> torch.Tensor:
        selected = embeddings.clone() if embeddings is not None else base_embeddings
        monkeypatch.setattr(
            MXCLR,
            "_encode_descriptions_with_sbert",
            staticmethod(
                lambda descriptions, model_name, max_length: selected[: len(descriptions)].clone()
            ),
        )
        return selected

    return _stub


@pytest.fixture(scope="function")
def mxclr_test_case(
    mxclr_dataset_factory,
    stub_mxclr_encoder,
) -> tuple[str, str, torch.Tensor, torch.Tensor, torch.Tensor]:
    data_dir, dataset_name, _ = mxclr_dataset_factory()
    stub_mxclr_encoder()
    z = torch.tensor(
        [
            [1.0, 0.0, 0.5],
            [0.8, 0.2, 0.4],
            [-0.3, 0.9, 0.1],
            [0.0, -0.4, 1.2],
        ],
        dtype=torch.float32,
    )
    labels = torch.tensor(
        [
            [1, 0, 1],
            [1, 0, 0],
            [0, 1, 0],
            [0, 1, 1],
        ],
        dtype=torch.float32,
    )
    g_soft = torch.tensor(
        [
            [1.0, 0.8, 0.2, 0.1],
            [0.8, 1.0, 0.3, 0.2],
            [0.2, 0.3, 1.0, 0.7],
            [0.1, 0.2, 0.7, 1.0],
        ],
        dtype=torch.float32,
    )
    return str(data_dir), dataset_name, z, labels, g_soft
