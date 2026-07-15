from __future__ import annotations

import pytest
import torch

from src.models.loss.agg.bertscore_f1 import (
    BERTScoreF1Graph,
    BERTScorePrecisionGraph,
    BERTScoreRecallGraph,
    BERTScoreUniformF1Graph,
)
from src.models.loss.mxclr import (
    MXCLR,
    _compute_mxclr_loss,
    _whiten_label_embeddings,
)


def test_build_label_embeddings_without_whitening_keeps_encoder_output(
    mxclr_dataset_factory,
    stub_mxclr_encoder,
) -> None:
    data_dir, dataset_name, _ = mxclr_dataset_factory()
    encoded = stub_mxclr_encoder()

    embeddings = MXCLR._build_label_embeddings(
        data_dir=data_dir,
        dataset_name=dataset_name,
        sbert_model_name="test-model",
        sbert_max_length=128,
        whitening=False,
    )

    assert torch.equal(embeddings, encoded[:3])


def test_whiten_label_embeddings_centers_and_whitens_encoded_matrix() -> None:
    embeddings = torch.tensor(
        [
            [1.0, 0.0],
            [0.0, 1.0],
            [0.0, 1.0],
            [-1.0, 0.0],
            [0.0, -1.0],
        ],
        dtype=torch.float32,
    )

    whitened = _whiten_label_embeddings(embeddings)
    covariance = whitened.T @ whitened / whitened.size(0)

    assert not torch.allclose(whitened, embeddings)
    assert torch.allclose(whitened.mean(dim=0), torch.zeros(2), atol=1e-6)
    assert torch.allclose(covariance, torch.eye(2), atol=1e-5)


def test_mxclr_aggs_declare_required_label_stats() -> None:
    assert BERTScoreF1Graph.required_label_stats() == frozenset({"npmi", "label_idf"})
    assert BERTScoreUniformF1Graph.required_label_stats() == frozenset({"npmi"})
    assert BERTScorePrecisionGraph.required_label_stats() == frozenset({"npmi", "label_idf"})
    assert BERTScoreRecallGraph.required_label_stats() == frozenset({"npmi", "label_idf"})


@pytest.mark.parametrize(
    ("agg_factory", "expect_symmetric", "expect_idf"),
    [
        (BERTScoreF1Graph, True, True),
        (BERTScoreUniformF1Graph, True, False),
        (BERTScorePrecisionGraph, False, True),
        (BERTScoreRecallGraph, False, True),
    ],
)
def test_mxclr_bertscore_aggs_autoload_required_label_stats(
    mxclr_dataset_factory,
    stub_mxclr_encoder,
    agg_factory,
    expect_symmetric: bool,
    expect_idf: bool,
) -> None:
    data_dir, dataset_name, _ = mxclr_dataset_factory(
        train_rows=[
            "doc1,1,0,1\n",
            "doc2,1,0,0\n",
            "doc3,0,1,0\n",
            "doc4,0,1,1\n",
        ],
    )
    stub_mxclr_encoder()
    labels = torch.tensor(
        [
            [1, 0, 1],
            [1, 0, 0],
            [0, 1, 0],
            [0, 1, 1],
        ],
        dtype=torch.float32,
    )

    loss_fn = MXCLR(
        data_dir=str(data_dir),
        dataset_name=dataset_name,
        agg=agg_factory(),
    )

    graph = loss_fn.score_graph(labels)

    assert loss_fn.label_npmi.shape == (3, 3)
    if expect_idf:
        assert loss_fn.label_idf.shape == (3,)
    else:
        assert loss_fn.label_idf.numel() == 0
    assert graph.shape == (4, 4)
    assert torch.isfinite(graph).all()
    if expect_symmetric:
        assert torch.allclose(graph, graph.T)
    else:
        assert not torch.allclose(graph, graph.T)
    assert torch.all((0.0 <= graph) & (graph <= 1.0))


def test_bertscore_directional_aggs_match_f1_components() -> None:
    labels = torch.tensor(
        [
            [1, 1, 0],
            [0, 0, 1],
        ],
        dtype=torch.float32,
    )
    label_embeddings = torch.tensor(
        [
            [1.0, 0.0],
            [0.0, 1.0],
            [1.0, 1.0],
        ],
        dtype=torch.float32,
    )
    npmi = torch.tensor(
        [
            [1.0, -1.0, 1.0],
            [-1.0, 1.0, -1.0],
            [1.0, -1.0, 1.0],
        ],
        dtype=torch.float32,
    )
    label_idf = torch.ones(3, dtype=torch.float32)

    bertscore_precision = BERTScorePrecisionGraph(transport_lambda=1.0)
    bertscore_recall = BERTScoreRecallGraph(transport_lambda=1.0)
    bertscore_f1 = BERTScoreF1Graph(transport_lambda=1.0)

    precision_graph = bertscore_precision(
        labels,
        label_embeddings,
        npmi=npmi,
        label_idf=label_idf,
    )
    recall_graph = bertscore_recall(
        labels,
        label_embeddings,
        npmi=npmi,
        label_idf=label_idf,
    )
    f1_graph = bertscore_f1(
        labels,
        label_embeddings,
        npmi=npmi,
        label_idf=label_idf,
    )

    assert torch.isclose(precision_graph[0, 1], torch.tensor(0.5))
    assert torch.isclose(recall_graph[0, 1], torch.tensor(1.0))
    assert torch.allclose(recall_graph, precision_graph.T)
    assert torch.isclose(f1_graph[0, 1], torch.tensor(2.0 / 3.0))


def test_bertscore_uniform_f1_uses_equal_label_weights() -> None:
    labels = torch.tensor(
        [
            [1, 1, 0],
            [0, 0, 1],
        ],
        dtype=torch.float32,
    )
    label_embeddings = torch.tensor(
        [
            [1.0, 0.0],
            [0.0, 1.0],
            [1.0, 1.0],
        ],
        dtype=torch.float32,
    )
    npmi = torch.tensor(
        [
            [1.0, -1.0, 1.0],
            [-1.0, 1.0, -1.0],
            [1.0, -1.0, 1.0],
        ],
        dtype=torch.float32,
    )
    label_idf = torch.tensor([3.0, 1.0, 1.0], dtype=torch.float32)

    weighted = BERTScoreF1Graph(transport_lambda=1.0)(
        labels,
        label_embeddings,
        npmi=npmi,
        label_idf=label_idf,
    )
    uniform = BERTScoreUniformF1Graph(transport_lambda=1.0)(
        labels,
        label_embeddings,
        npmi=npmi,
    )

    assert torch.isclose(weighted[0, 1], torch.tensor(6.0 / 7.0))
    assert torch.isclose(uniform[0, 1], torch.tensor(2.0 / 3.0))
    assert not torch.allclose(weighted, uniform)


def test_mxclr_forward_with_direct_graph_returns_finite_scalar(
    mxclr_dataset_factory,
    stub_mxclr_encoder,
) -> None:
    data_dir, dataset_name, _ = mxclr_dataset_factory()
    stub_mxclr_encoder()
    z = torch.tensor(
        [
            [2.0, 0.1],
            [1.8, 0.2],
            [0.2, 1.7],
            [0.0, 1.9],
        ],
        dtype=torch.float32,
    )
    graph = torch.tensor(
        [
            [1.0, 0.95, 0.05, 0.01],
            [0.95, 1.0, 0.04, 0.01],
            [0.05, 0.04, 1.0, 0.9],
            [0.01, 0.01, 0.9, 1.0],
        ],
        dtype=torch.float32,
    )
    loss_fn = MXCLR(
        data_dir=str(data_dir),
        dataset_name=dataset_name,
        agg=BERTScoreF1Graph(),
    )

    out = loss_fn(z, graph)

    assert torch.isfinite(out)


def test_mxclr_loss_uses_cosine_similarity() -> None:
    z = torch.nn.functional.normalize(
        torch.tensor(
            [
                [2.0, 0.1],
                [1.8, 0.2],
                [0.2, 1.7],
                [0.0, 1.9],
            ],
            dtype=torch.float32,
        ),
        dim=1,
    )
    graph = torch.tensor(
        [
            [1.0, 0.95, 0.05, 0.01],
            [0.95, 1.0, 0.04, 0.01],
            [0.05, 0.04, 1.0, 0.9],
            [0.01, 0.01, 0.9, 1.0],
        ],
        dtype=torch.float32,
    )

    actual = _compute_mxclr_loss(
        z=z,
        g_soft=graph,
        instance_temperature=0.1,
        graph_temperature=0.2,
    )

    logits = (z @ z.T) / 0.1
    off_diag = ~torch.eye(z.size(0), dtype=torch.bool)
    log_p = torch.nn.functional.log_softmax(logits.masked_fill(~off_diag, float("-inf")), dim=1)
    s_logits = graph / 0.2
    s = torch.nn.functional.softmax(s_logits.masked_fill(~off_diag, float("-inf")), dim=1)
    expected = (
        -(s.masked_fill(~off_diag, 0.0) * log_p.masked_fill(~off_diag, 0.0)).sum(dim=1).mean()
    )

    assert torch.allclose(actual, expected)


def test_mxclr_forward_is_invariant_to_rowwise_feature_scaling(
    mxclr_dataset_factory,
    stub_mxclr_encoder,
) -> None:
    data_dir, dataset_name, _ = mxclr_dataset_factory()
    stub_mxclr_encoder()
    z = torch.tensor(
        [
            [2.0, 0.1],
            [1.8, 0.2],
            [0.2, 1.7],
            [0.0, 1.9],
        ],
        dtype=torch.float32,
    )
    scales = torch.tensor([[2.0], [0.5], [1.5], [3.0]], dtype=torch.float32)
    graph = torch.tensor(
        [
            [1.0, 0.95, 0.05, 0.01],
            [0.95, 1.0, 0.04, 0.01],
            [0.05, 0.04, 1.0, 0.9],
            [0.01, 0.01, 0.9, 1.0],
        ],
        dtype=torch.float32,
    )
    loss_fn = MXCLR(
        data_dir=str(data_dir),
        dataset_name=dataset_name,
        agg=BERTScoreF1Graph(),
    )

    assert torch.allclose(loss_fn(z, graph), loss_fn(z * scales, graph), atol=1e-6)
