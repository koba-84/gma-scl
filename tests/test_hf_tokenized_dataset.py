from __future__ import annotations

from typing import Any
from unittest import mock

import torch
from datasets import Dataset

from src.data.components.hf_tokenized_dataset import TokenizedTorchDataset


def test_tokenized_torch_dataset_reuses_tensor_backed_rows() -> None:
    split = Dataset.from_dict(
        {
            "input_ids": [[1, 2, 3]],
            "attention_mask": [[1, 1, 1]],
            "labels": [[1.0, 0.0]],
            "is_empty_text": [False],
            "text": ["hello"],
        }
    )
    split.set_format(
        type="torch",
        columns=["input_ids", "attention_mask", "labels", "is_empty_text"],
        output_all_columns=True,
    )

    dataset = TokenizedTorchDataset(split, text_column="text")

    original_as_tensor = torch.as_tensor

    def _guard_as_tensor(value: Any, *args: Any, **kwargs: Any) -> torch.Tensor:
        if isinstance(value, torch.Tensor):
            raise AssertionError("tensor-backed row must not be rebuilt with torch.as_tensor")
        return original_as_tensor(value, *args, **kwargs)

    with mock.patch(
        "src.data.components.hf_tokenized_dataset.torch.as_tensor", side_effect=_guard_as_tensor
    ):
        features, labels, text = dataset[0]

    row = split[0]
    assert isinstance(row["input_ids"], torch.Tensor)
    assert isinstance(row["attention_mask"], torch.Tensor)
    assert isinstance(row["labels"], torch.Tensor)
    assert features["empty_text_mask"].dtype == torch.bool
    assert features["input_ids"].dtype == torch.long
    assert features["attention_mask"].dtype == torch.long
    assert labels.dtype == torch.float32
    assert text == "hello"
