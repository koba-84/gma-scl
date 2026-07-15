from __future__ import annotations

from src.models.contrastive_module import _contrastive_metric_axis_definitions


def test_contrastive_metric_axis_definitions_use_explicit_loss_metrics() -> None:
    definitions = _contrastive_metric_axis_definitions()

    assert definitions == (
        ("contrastive/epoch", {}),
        (
            "contrastive/train/loss",
            {"step_metric": "contrastive/epoch", "step_sync": True},
        ),
        (
            "contrastive/val/loss",
            {"step_metric": "contrastive/epoch", "step_sync": True},
        ),
    )
    assert all("*" not in name for name, _ in definitions)
