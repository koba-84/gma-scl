from __future__ import annotations

from dataclasses import dataclass

import torch
from datasets import Dataset as HFDataset
from datasets import DatasetDict
from torch.utils.data import Dataset


@dataclass(frozen=True)
class TokenizedDatasetBundle:
    """Bundle of tokenized splits plus the schema needed by downstream datamodules."""

    dataset_dict: DatasetDict
    label_columns: list[str]
    text_column: str


class TokenizedTorchDataset(Dataset[tuple[dict[str, torch.Tensor], torch.Tensor, str]]):
    """Torch Dataset wrapper over a tokenized Hugging Face split."""

    def __init__(self, split: HFDataset, text_column: str = "text") -> None:
        self.split = split
        self.text_column = text_column

    def __len__(self) -> int:
        return len(self.split)

    @staticmethod
    def _coerce_tensor(value: object, *, dtype: torch.dtype) -> torch.Tensor:
        if isinstance(value, torch.Tensor):
            return value if value.dtype == dtype else value.to(dtype=dtype)
        return torch.as_tensor(value, dtype=dtype)

    def __getitem__(self, idx: int) -> tuple[dict[str, torch.Tensor], torch.Tensor, str]:
        row = self.split[int(idx)]
        features = {
            "input_ids": self._coerce_tensor(row["input_ids"], dtype=torch.long),
            "attention_mask": self._coerce_tensor(row["attention_mask"], dtype=torch.long),
            "empty_text_mask": self._coerce_tensor(
                row.get("is_empty_text", False),
                dtype=torch.bool,
            ),
        }
        labels = self._coerce_tensor(row["labels"], dtype=torch.float32)
        text = str(row.get(self.text_column, ""))
        return features, labels, text
