from __future__ import annotations

import csv
from pathlib import Path
import shutil
from typing import List, Tuple

import torch
from torch.utils.data import Dataset


class ClassificationDataset(Dataset[Tuple[str, torch.Tensor]]):
    """Dataset for multi-label CSV files.

    Expected format:
    - First column: input text
    - Remaining columns: binary labels (0/1 or float values)
    """

    def __init__(
        self,
        file_path: str | Path,
        label_columns: list[str],
    ) -> None:
        self.file_path = Path(file_path)
        self.label_columns = list(label_columns)

        self._items: List[Tuple[str, torch.Tensor]] = []
        self._load()

    def _load(self) -> None:
        if not self.file_path.exists():
            raise FileNotFoundError(f"Dataset file not found: {self.file_path}")

        with self.file_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            if fieldnames is None:
                raise ValueError(f"Invalid CSV in {self.file_path}: missing header.")
            if len(fieldnames) < 2:
                raise ValueError(
                    f"Invalid CSV in {self.file_path}: expected text + at least one label column."
                )
            text_column = fieldnames[0]
            for label_col in self.label_columns:
                if label_col not in fieldnames:
                    raise ValueError(
                        f"Missing label column '{label_col}' in {self.file_path}."
                    )

            for line_idx, row in enumerate(reader, start=2):
                text = (row.get(text_column) or "").strip()
                labels: list[float] = []
                for label_col in self.label_columns:
                    raw_value = row.get(label_col)
                    if raw_value is None:
                        raise ValueError(
                            f"Missing value for label column '{label_col}' "
                            f"in {self.file_path} at line {line_idx}."
                        )
                    try:
                        labels.append(float(raw_value))
                    except ValueError as e:
                        raise ValueError(
                            f"Invalid label value '{raw_value}' for column '{label_col}' "
                            f"in {self.file_path} at line {line_idx}."
                        ) from e

                label_tensor = torch.tensor(labels, dtype=torch.float32)
                self._items.append((text, label_tensor))

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, idx: int) -> Tuple[str, torch.Tensor]:
        return self._items[idx]


if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parents[3]
    tmp_dir = root_dir / "tmp" / "classification_dataset_self_test"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    try:
        valid_csv = tmp_dir / "valid.csv"
        valid_csv.write_text(
            "text,label_a,label_b\n"
            "sample one,1,0\n"
            " sample two ,0,1\n",
            encoding="utf-8",
        )
        dataset = ClassificationDataset(file_path=valid_csv, label_columns=["label_a", "label_b"])
        assert len(dataset) == 2
        text, labels = dataset[1]
        assert text == "sample two"
        assert labels.tolist() == [0.0, 1.0]

        try:
            _ = ClassificationDataset(file_path=tmp_dir / "not-found.csv", label_columns=["label_a"])
        except FileNotFoundError:
            pass
        else:
            raise AssertionError("Missing dataset file must raise FileNotFoundError")

        missing_col_csv = tmp_dir / "missing_col.csv"
        missing_col_csv.write_text("text,label_a\nsample,1\n", encoding="utf-8")
        try:
            _ = ClassificationDataset(
                file_path=missing_col_csv,
                label_columns=["label_a", "label_b"],
            )
        except ValueError as exc:
            assert "Missing label column 'label_b'" in str(exc)
        else:
            raise AssertionError("Missing label column must raise ValueError")

        invalid_value_csv = tmp_dir / "invalid_value.csv"
        invalid_value_csv.write_text("text,label_a\nsample,abc\n", encoding="utf-8")
        try:
            _ = ClassificationDataset(file_path=invalid_value_csv, label_columns=["label_a"])
        except ValueError as exc:
            assert "Invalid label value 'abc'" in str(exc)
        else:
            raise AssertionError("Invalid label value must raise ValueError")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    print("ClassificationDataset self-test passed.")
