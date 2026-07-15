- [x] 1.1 Add MultiScaleMXCLR implementation, public export, Hydra config, pytest coverage, and synced training specs.

Validation:

- `PROJECT_ROOT=$(pwd) uv run pytest tests/losses/test_multi_scale_mxclr_loss.py tests/test_configs.py -q`
- `PROJECT_ROOT=$(pwd) uv run python src/train.py --cfg job --resolve contrastive/model=multi_scale_mxclr`
- `uv run openspec validate add-multiscale-mxclr --strict`
- `PROJECT_ROOT=$(pwd) uv run pre-commit run -a`
- `scripts/test.sh` is intentionally not required for this loss-only change because it does not modify GPU runtime, trainer, or data execution paths.

Task commit: f16ec3e
