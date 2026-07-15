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
from src.models.loss.mxclr_rank import MXCLRRank, _compute_mxclr_rank_loss


def _mxclr_rank_agg(agg: str) -> nn.Module:
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
    ("agg", "expect_symmetric"),
    [
        ("BERTScore_F1", True),
        ("BERTScore_F1_Uniform", True),
        ("BERTScore_Precision", False),
        ("BERTScore_Recall", False),
    ],
)
def test_mxclr_rank_forward_supports_mxclr_and_bertscore_aggs(
    agg: str,
    expect_symmetric: bool,
    mxclr_test_case: tuple[str, str, torch.Tensor, torch.Tensor, torch.Tensor],
) -> None:
    data_dir, dataset_name, z, labels, g_soft = mxclr_test_case
    loss_fn = MXCLRRank(
        data_dir=data_dir,
        dataset_name=dataset_name,
        agg=_mxclr_rank_agg(agg),
    )

    graph = loss_fn.score_graph(labels)
    out_labels = loss_fn(z, labels)
    out_graph = loss_fn(z, g_soft)

    assert graph.shape == (4, 4)
    assert torch.isfinite(graph).all()
    if expect_symmetric:
        assert torch.allclose(graph, graph.T)
    else:
        assert not torch.allclose(graph, graph.T)
    assert torch.isfinite(out_labels)
    assert torch.isfinite(out_graph)


def test_mxclr_rank_lambda_zero_matches_mxclr(
    mxclr_test_case: tuple[str, str, torch.Tensor, torch.Tensor, torch.Tensor],
) -> None:
    data_dir, dataset_name, z, labels, _ = mxclr_test_case
    mxclr = MXCLR(
        data_dir=data_dir,
        dataset_name=dataset_name,
        instance_temperature=0.1,
        graph_temperature=0.1,
        agg=BERTScoreF1Graph(),
    )
    mxclr_rank = MXCLRRank(
        data_dir=data_dir,
        dataset_name=dataset_name,
        instance_temperature=0.1,
        graph_temperature=0.1,
        lambda_rank=0.0,
        agg=BERTScoreF1Graph(),
    )

    assert torch.allclose(mxclr(z, labels), mxclr_rank(z, labels))


def test_mxclr_rank_forward_is_invariant_to_rowwise_feature_scaling(
    mxclr_test_case: tuple[str, str, torch.Tensor, torch.Tensor, torch.Tensor],
) -> None:
    data_dir, dataset_name, z, _, g_soft = mxclr_test_case
    scales = torch.tensor([[2.0], [0.5], [1.5], [3.0]], dtype=torch.float32)
    loss_fn = MXCLRRank(
        data_dir=data_dir,
        dataset_name=dataset_name,
        agg=BERTScoreF1Graph(),
    )

    assert torch.allclose(loss_fn(z, g_soft), loss_fn(z * scales, g_soft), atol=1e-6)


def test_compute_mxclr_rank_loss_uses_single_lambda_without_batch_normalization(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        "src.models.loss.mxclr_rank._compute_mxclr_loss",
        lambda **_: torch.tensor(2.0),
    )
    monkeypatch.setattr(
        "src.models.loss.mxclr_rank.compute_listmle_loss",
        lambda **_: torch.tensor(3.0),
    )

    z = torch.randn(4, 3)
    g_soft = torch.randn(4, 4)

    loss = _compute_mxclr_rank_loss(
        z=z,
        g_soft=g_soft,
        instance_temperature=0.1,
        graph_temperature=0.2,
        rank_temperature=0.3,
        lambda_rank=0.5,
    )

    assert loss == pytest.approx(3.5)


def test_compute_mxclr_rank_loss_scales_listmle_with_rank_temperature(
    monkeypatch,
) -> None:
    captured: dict[str, torch.Tensor] = {}
    monkeypatch.setattr(
        "src.models.loss.mxclr_rank._compute_mxclr_loss",
        lambda **_: torch.tensor(2.0),
    )

    def _fake_listmle_loss(**kwargs) -> torch.Tensor:
        captured["student_scores"] = kwargs["student_scores"]
        return torch.tensor(3.0)

    monkeypatch.setattr("src.models.loss.mxclr_rank.compute_listmle_loss", _fake_listmle_loss)

    z = torch.tensor([[1.0, 0.0], [0.0, 1.0]], dtype=torch.float32)
    g_soft = torch.ones(2, 2, dtype=torch.float32)

    _compute_mxclr_rank_loss(
        z=z,
        g_soft=g_soft,
        instance_temperature=0.1,
        graph_temperature=0.2,
        rank_temperature=0.5,
        lambda_rank=0.5,
    )

    assert torch.allclose(captured["student_scores"], (z @ z.T) / 0.5)


@pytest.mark.parametrize(
    ("factory", "message"),
    [
        (
            lambda: MXCLRRank(
                data_dir="missing_root",
                dataset_name="aapd",
                lambda_rank=-0.1,
                agg=BERTScoreF1Graph(),
            ),
            "lambda_rank must be >= 0",
        ),
        (
            lambda: MXCLRRank(
                data_dir="missing_root",
                dataset_name="aapd",
                rank_temperature=0.0,
                agg=BERTScoreF1Graph(),
            ),
            "rank_temperature must be > 0",
        ),
        (
            lambda: MXCLRRank(
                data_dir="missing_root",
                dataset_name="aapd",
                agg=None,
            ),
            "agg is required",
        ),
    ],
)
def test_mxclr_rank_init_validates_required_arguments(
    factory: Callable[[], MXCLRRank],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        factory()
