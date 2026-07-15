from __future__ import annotations

from collections.abc import Callable

import pytest
import torch
from torch import nn

from src.models.loss.agg.bertscore_f1 import (
    BERTScoreF1Graph,
    BERTScorePrecisionGraph,
    BERTScoreRecallGraph,
    BERTScoreUniformF1Graph,
)
from src.models.loss.mxclr import MXCLR


def _mxclr_agg(agg: str) -> nn.Module:
    if agg == "BERTScore_F1":
        return BERTScoreF1Graph()
    if agg == "BERTScore_F1_Uniform":
        return BERTScoreUniformF1Graph()
    if agg == "BERTScore_Precision":
        return BERTScorePrecisionGraph()
    if agg == "BERTScore_Recall":
        return BERTScoreRecallGraph()
    raise AssertionError(f"Unsupported test agg: {agg}")


@pytest.mark.parametrize(
    "agg",
    [
        "BERTScore_F1",
        "BERTScore_F1_Uniform",
        "BERTScore_Precision",
        "BERTScore_Recall",
    ],
)
def test_mxclr_score_graph_and_forward(
    agg: str,
    mxclr_test_case: tuple[str, str, torch.Tensor, torch.Tensor, torch.Tensor],
) -> None:
    data_dir, dataset_name, z, labels, g_soft = mxclr_test_case
    loss_fn = MXCLR(
        data_dir=data_dir,
        dataset_name=dataset_name,
        agg=_mxclr_agg(agg),
    )

    graph = loss_fn.score_graph(labels)
    assert graph.shape == (4, 4)
    assert torch.isfinite(graph).all()
    if agg in {"BERTScore_Precision", "BERTScore_Recall"}:
        counterpart = MXCLR(
            data_dir=data_dir,
            dataset_name=dataset_name,
            agg=_mxclr_agg(
                "BERTScore_Recall" if agg == "BERTScore_Precision" else "BERTScore_Precision"
            ),
        )
        counterpart_graph = counterpart.score_graph(labels)
        assert torch.allclose(graph, counterpart_graph.T)
    else:
        assert torch.allclose(graph, graph.T)
    assert torch.all((0.0 <= graph) & (graph <= 1.0))

    out_labels = loss_fn(z, labels)
    out_graph = loss_fn(z, g_soft)
    assert out_labels.ndim == 0
    assert out_graph.ndim == 0
    assert torch.isfinite(out_labels)
    assert torch.isfinite(out_graph)


def test_mxclr_forward_rejects_batch_size_below_two(
    mxclr_test_case: tuple[str, str, torch.Tensor, torch.Tensor, torch.Tensor],
) -> None:
    data_dir, dataset_name, z, labels, _ = mxclr_test_case
    loss_fn = MXCLR(
        data_dir=data_dir,
        dataset_name=dataset_name,
        agg=_mxclr_agg("BERTScore_F1"),
    )
    with pytest.raises(RuntimeError, match="batch_size >= 2"):
        loss_fn(z[:1], labels[:1])


@pytest.mark.parametrize(
    ("factory", "message"),
    [
        (
            lambda: MXCLR(
                data_dir="missing_root",
                dataset_name="aapd",
                sbert_max_length=0,
                agg=_mxclr_agg("BERTScore_F1"),
            ),
            "sbert_max_length must be > 0",
        ),
        (
            lambda: MXCLR(
                data_dir="missing_root",
                dataset_name="aapd",
            ),
            "agg is required",
        ),
    ],
)
def test_mxclr_init_validates_required_arguments(
    factory: Callable[[], MXCLR],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        factory()


def test_mxclr_init_rejects_missing_dataset_label_descriptions() -> None:
    with pytest.raises(FileNotFoundError, match="Label description file not found"):
        MXCLR(
            data_dir="missing_root",
            dataset_name="aapd",
            agg=_mxclr_agg("BERTScore_F1"),
        )


def test_mxclr_init_supports_non_aapd_dataset_with_dataset_scoped_json(
    tmp_path,
    stub_mxclr_encoder,
) -> None:
    data_root = tmp_path / "data"
    dataset_dir = data_root / "custom"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    (dataset_dir / "label_descriptions.json").write_text(
        """{"labels":[{"index":1,"description":"alpha"},{"index":2,"description":"beta"}]}""",
        encoding="utf-8",
    )
    (dataset_dir / "train.csv").write_text(
        "text,label_0,label_1\ndoc1,1,0\ndoc2,0,1\n",
        encoding="utf-8",
    )
    stub_mxclr_encoder(torch.tensor([[1.0, 0.0], [0.0, 1.0]], dtype=torch.float32))

    loss_fn = MXCLR(
        data_dir=str(data_root),
        dataset_name="custom",
        agg=_mxclr_agg("BERTScore_F1"),
    )

    assert loss_fn.label_embeddings.shape == (2, 2)
