import torch
from torch.utils.data import Dataset

from src.data.multi_dataset_datamodule import (
    MultiDatasetSampleDataset,
    MultiDatasetSpec,
    _collate_multi_dataset,
)


class _SyntheticDataset(Dataset[tuple[dict[str, torch.Tensor], torch.Tensor, str]]):
    def __init__(self, label_count: int, size: int) -> None:
        self.items = []
        for index in range(size):
            self.items.append(
                (
                    {
                        "input_ids": torch.tensor([index, 1]),
                        "attention_mask": torch.ones(2, dtype=torch.long),
                        "empty_text_mask": torch.tensor(False),
                    },
                    torch.nn.functional.one_hot(
                        torch.tensor(index % label_count), num_classes=label_count
                    ).float(),
                    f"sample-{index}",
                )
            )

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index: int) -> tuple[dict[str, torch.Tensor], torch.Tensor, str]:
        return self.items[index]


def test_multi_dataset_sample_dataset_offsets_local_labels() -> None:
    specs = (
        MultiDatasetSpec("a", 0, ("a0", "a1"), 0),
        MultiDatasetSpec("b", 1, ("b0",), 2),
    )
    dataset = MultiDatasetSampleDataset(
        [_SyntheticDataset(2, 1), _SyntheticDataset(1, 1)],
        specs,
    )

    first = dataset[0]
    second = dataset[1]

    assert first[2] == 0
    assert second[2] == 1
    assert first[1].shape == (3,)
    assert second[1].shape == (3,)
    assert torch.equal(first[1], torch.tensor([1.0, 0.0, 0.0]))
    assert torch.equal(second[1], torch.tensor([0.0, 0.0, 1.0]))


def test_multi_dataset_collate_keeps_dataset_ids_and_global_labels() -> None:
    specs = (
        MultiDatasetSpec("a", 0, ("a0",), 0),
        MultiDatasetSpec("b", 1, ("b0",), 1),
    )
    dataset = MultiDatasetSampleDataset(
        [_SyntheticDataset(1, 1), _SyntheticDataset(1, 1)],
        specs,
    )
    batch = _collate_multi_dataset([dataset[0], dataset[1]])

    inputs, labels = batch
    assert torch.equal(inputs["dataset_id"], torch.tensor([0, 1]))
    assert labels.shape == (2, 2)
    assert torch.equal(labels, torch.eye(2))
