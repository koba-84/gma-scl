import json
import sys
import types

import torch

from src.models.loss.multi_dataset_mxclr import (
    MultiDatasetMXCLR,
    build_semantic_graph,
)


def test_build_semantic_graph_supports_cross_dataset_label_sets() -> None:
    embeddings = torch.tensor(
        [[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]],
        dtype=torch.float32,
    )
    labels = torch.tensor(
        [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
        dtype=torch.float32,
    )

    graph = build_semantic_graph(labels, embeddings)

    assert graph.shape == (3, 3)
    assert torch.allclose(torch.diag(graph), torch.zeros(3))
    assert graph[0, 1] > graph[0, 2]
    assert torch.allclose(graph, graph.T, atol=1e-6)


def test_build_semantic_graph_uses_l2norm_weighted_multilabel_semantic_f1() -> None:
    embeddings = torch.tensor(
        [[2.0, 0.0], [0.8, 0.6], [0.0, 3.0]],
        dtype=torch.float32,
    )
    labels = torch.tensor(
        [[1.0, 1.0, 0.0], [0.0, 1.0, 1.0]],
        dtype=torch.float32,
    )

    graph = build_semantic_graph(labels, embeddings)
    precision = (1.0 * 1.0 + 0.6 * 3.0) / (1.0 + 3.0)
    recall = (0.8 * 2.0 + 1.0 * 1.0) / (2.0 + 1.0)
    expected = 2.0 * precision * recall / (precision + recall)

    assert torch.allclose(graph[0, 1], torch.tensor(expected), atol=1e-6)
    assert torch.allclose(graph[0, 1], graph[1, 0], atol=1e-6)


def test_build_semantic_graph_handles_empty_label_rows() -> None:
    labels = torch.tensor([[0.0, 0.0], [1.0, 0.0]], dtype=torch.float32)
    graph = build_semantic_graph(labels, torch.eye(2))

    assert torch.equal(graph[0], torch.zeros(2))
    assert torch.equal(graph[:, 0], torch.zeros(2))


def test_multi_dataset_mxclr_has_no_label_statistics_contract() -> None:
    loss = MultiDatasetMXCLR(torch.eye(3), instance_temperature=0.2, graph_temperature=0.3)
    z = torch.randn(3, 4)
    labels = torch.eye(3)

    value = loss(z, labels)

    assert value.ndim == 0
    assert torch.isfinite(value)
    assert not hasattr(loss, "label_npmi")
    assert not hasattr(loss, "label_idf")


def test_multi_dataset_mxclr_loads_dataset_description_embeddings(monkeypatch, tmp_path) -> None:
    fake_module = types.ModuleType("sentence_transformers")

    class _FakeSentenceTransformer:
        def __init__(self, _model_name: str) -> None:
            self.max_seq_length = 0

        def encode(self, descriptions, **_kwargs):
            return torch.ones((len(descriptions), 2), dtype=torch.float32)

    setattr(fake_module, "SentenceTransformer", _FakeSentenceTransformer)
    monkeypatch.setitem(sys.modules, "sentence_transformers", fake_module)

    data_dir = tmp_path / "data"
    for dataset_name in ("a", "b"):
        dataset_dir = data_dir / dataset_name
        dataset_dir.mkdir(parents=True)
        (dataset_dir / "label_descriptions.json").write_text(
            json.dumps(
                {
                    "labels": [
                        {"index": 0, "description": f"{dataset_name} label"},
                    ]
                }
            ),
            encoding="utf-8",
        )

    loss = MultiDatasetMXCLR.from_dataset_descriptions(
        data_dir=data_dir,
        dataset_names=["a", "b"],
        model_name="fake",
        max_length=8,
        whitening=True,
    )
    graph = loss.score_graph(torch.eye(2))
    value = loss(torch.randn(2, 3), torch.eye(2))

    assert loss.label_embeddings.shape == (2, 2)
    assert graph.shape == (2, 2)
    assert torch.isfinite(value)
