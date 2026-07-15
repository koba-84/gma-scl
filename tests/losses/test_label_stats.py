from __future__ import annotations

import torch

from src.models.loss.components.label_stats import compute_yules_q


def test_compute_yules_q_uses_haldane_anscombe_correction(mxclr_dataset_factory) -> None:
    data_dir, dataset_name, _ = mxclr_dataset_factory(
        train_rows=[
            "doc1,1,0,1\n",
            "doc2,1,0,0\n",
            "doc3,0,1,0\n",
            "doc4,0,1,1\n",
        ],
    )

    yules_q = compute_yules_q(data_dir=data_dir, dataset_name=dataset_name)

    expected = torch.tensor(
        [
            [1.0, 0.03846154, 0.5],
            [0.03846154, 1.0, 0.5],
            [0.5, 0.5, 1.0],
        ],
        dtype=torch.float32,
    )
    assert yules_q.shape == (3, 3)
    assert torch.isfinite(yules_q).all()
    assert torch.allclose(yules_q, expected)
    assert torch.all((0.0 <= yules_q) & (yules_q <= 1.0))
