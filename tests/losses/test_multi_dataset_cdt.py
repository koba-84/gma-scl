import pytest
import torch

from src.models.loss.multi_dataset_cdt import (
    MultiDatasetCDT,
    covariance_adjusted_scores,
)


def test_cdt_same_domain_score_is_direct_cosine(monkeypatch) -> None:
    z = torch.tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    dataset_ids = torch.zeros(3, dtype=torch.long)
    covariances = torch.stack([2.0 * torch.eye(2), 4.0 * torch.eye(2)])

    def fail_if_called(*_args, **_kwargs):
        raise AssertionError("same-domain scoring must not call torch.einsum")

    monkeypatch.setattr(torch, "einsum", fail_if_called)
    scores = covariance_adjusted_scores(z, dataset_ids, covariances)
    normalized = torch.nn.functional.normalize(z, dim=1)

    assert torch.allclose(scores, normalized @ normalized.T)


def test_cdt_same_domain_cosine_matches_aninfonce_quadratic_softmax() -> None:
    z = torch.randn(4, 3)
    dataset_ids = torch.zeros(4, dtype=torch.long)
    covariances = torch.stack([2.0 * torch.eye(3)])
    normalized = torch.nn.functional.normalize(z, dim=1)

    scores = covariance_adjusted_scores(z, dataset_ids, covariances)
    quadratic_scores = -0.5 * (
        (normalized[:, None, :] - normalized[None, :, :]).square().sum(dim=-1)
    )

    assert torch.allclose(
        torch.softmax(scores, dim=1),
        torch.softmax(quadratic_scores, dim=1),
        atol=1e-6,
    )


def test_cdt_cross_domain_score_matches_symmetric_covariance_reference() -> None:
    z = torch.tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    dataset_ids = torch.tensor([0, 0, 1])
    covariances = torch.stack(
        [torch.diag(torch.tensor([2.0, 3.0])), torch.diag(torch.tensor([4.0, 5.0]))]
    )
    normalized = torch.nn.functional.normalize(z, dim=1)
    difference = normalized[:, None, :] - normalized[None, :, :]
    covariance_a = covariances[dataset_ids]
    covariance_b = covariances[dataset_ids]
    quadratic_a = torch.einsum("abd,ade,abe->ab", difference, covariance_a, difference)
    quadratic_b = torch.einsum("abd,bde,abe->ab", difference, covariance_b, difference)
    reference = torch.where(
        dataset_ids[:, None] == dataset_ids[None, :],
        normalized @ normalized.T,
        -0.25 * (quadratic_a + quadratic_b),
    )

    scores = covariance_adjusted_scores(z, dataset_ids, covariances)

    assert torch.allclose(scores, reference)
    assert torch.allclose(scores, scores.T)


def test_cdt_cross_domain_scores_reuse_unordered_pairs(monkeypatch) -> None:
    z = torch.randn(7, 4)
    dataset_ids = torch.tensor([0, 1, 2, 0, 2, 1, 0])
    covariances = torch.stack(
        [
            torch.diag(torch.tensor([1.0, 2.0, 3.0, 4.0])),
            torch.diag(torch.tensor([2.0, 3.0, 4.0, 5.0])),
            torch.diag(torch.tensor([3.0, 4.0, 5.0, 6.0])),
        ]
    )
    normalized = torch.nn.functional.normalize(z, dim=1)
    reference = normalized @ normalized.T
    for row in range(z.size(0)):
        for column in range(z.size(0)):
            if dataset_ids[row] == dataset_ids[column]:
                continue
            metric = 0.5 * (covariances[dataset_ids[row]] + covariances[dataset_ids[column]])
            difference = normalized[row] - normalized[column]
            reference[row, column] = -0.5 * (difference @ metric @ difference)

    einsum_calls = 0
    original_einsum = torch.einsum

    def counted_einsum(*args, **kwargs):
        nonlocal einsum_calls
        einsum_calls += 1
        return original_einsum(*args, **kwargs)

    monkeypatch.setattr(torch, "einsum", counted_einsum)
    scores = covariance_adjusted_scores(z, dataset_ids, covariances)

    assert torch.allclose(scores, reference, atol=1e-6, rtol=1e-6)
    assert einsum_calls == 3


def test_multi_dataset_cdt_preserves_semantic_target_and_gradients() -> None:
    loss = MultiDatasetCDT(
        num_domains=2,
        embedding_dim=2,
        label_embeddings=torch.eye(3),
        instance_temperature=0.1,
        graph_temperature=0.01,
    )
    loss.set_domain_covariances(torch.stack([torch.eye(2), 2.0 * torch.eye(2)]))
    z = torch.randn(3, 2, requires_grad=True)
    labels = torch.eye(3)
    dataset_ids = torch.tensor([0, 1, 0])

    value = loss(z, labels, dataset_ids)
    value.backward()

    assert value.ndim == 0
    assert torch.isfinite(value)
    assert z.grad is not None
    assert torch.isfinite(z.grad).all()


def test_multi_dataset_cdt_rejects_uninitialized_covariance() -> None:
    loss = MultiDatasetCDT(num_domains=2, embedding_dim=2, label_embeddings=torch.eye(3))

    with pytest.raises(RuntimeError, match="covariances are not initialized"):
        loss(torch.randn(3, 2), torch.eye(3), torch.tensor([0, 1, 0]))
