# multi-label-supcon

This is an anonymized research artifact prepared for peer review.

This is a research repository for Multi-Label Supervised Contrastive Learning. It uses Hydra for experiment configuration and PyTorch Lightning for contrastive pretraining and classification evaluation.

The repository prioritizes reproducibility: the same Git commit, Hydra configuration, and seed should reproduce the same result.

## Overview

- Experiment environment based on Python 3.12 and uv
- Multi-label text classification with a RoBERTa encoder
- Two-stage workflow: contrastive stage followed by classification stage
- Dataset configurations for AAPD, RCV1, Reuters-21578, and UK-LEX
- W&B logging for resolved configs, primary metrics, and test score artifacts

## Repository Layout

```text
configs/
  train.yaml                  # Top-level Hydra entry config
  contrastive/                # Contrastive-stage data/model/sampler configs
  classification/             # Classification-stage data/strategy/loss configs
  data/                       # Shared dataset selection for both stages
  hparams_search/             # Hydra multirun / sweep configs
  logger/                     # Logger configs, including W&B
  trainer/                    # Trainer configs for cpu/gpu/ddp/mps
src/
  train.py                    # Training and evaluation entrypoint
  data/                       # Tokenized datamodules and dataset cache
  models/                     # LightningModules, encoder, and loss implementations
  utils/                      # Logging, Hydra instantiation, and W&B config helpers
tests/
  losses/                     # Regression tests for loss implementations
  property/                   # Hypothesis property-based tests
  integration/                # Data and training integration tests
scripts/
  test.sh                     # GPU-based execution check
```

## Setup

The source of truth for dependencies is `pyproject.toml` plus `uv.lock`. `requirements.txt` and `environment.yaml` are not used in the current workflow.

```bash
uv sync
```

Always run commands through the uv environment.

```bash
uv run python src/train.py --cfg job --resolve
```

PyTorch and torchvision are configured to resolve from the official PyTorch cu124 wheel index. GPU execution is expected to run on the validated local machine environment for this repository.

## Data

Dataset CSV files are not included in this anonymized artifact. Prepare each dataset under its own license or access terms and place files in this layout:

```text
data/<dataset_name>/train.csv
data/<dataset_name>/dev.csv
data/<dataset_name>/test.csv
```

Each CSV must contain an `abstract` text column followed by binary multi-label columns. The bundled `data/aapd/label_descriptions.json` contains generated label descriptions with source URLs recorded in the file.

## Training And Evaluation

The default `configs/train.yaml` workflow runs the stages in this order:

1. contrastive stage
2. classification stage

By default, the contrastive stage has `test: false`, while the classification stage has `test: True`. Classification test evaluation prefers the checkpoint with the best validation macro-F1.

Minimal run:

```bash
uv run python src/train.py
```

CPU config check or lightweight run:

```bash
uv run python src/train.py trainer=cpu contrastive.trainer.max_epochs=1 classification.trainer.max_epochs=1
```

Local GPU execution check:

```bash
scripts/test.sh
```

`scripts/test.sh` requires a GPU. Its log is written to `tmp/test.log`.

## Configuration Examples

Switch datasets:

```bash
uv run python src/train.py data=rcv1
uv run python src/train.py data=reuters21578
uv run python src/train.py data=uklex
```

Switch contrastive losses:

```bash
uv run python src/train.py contrastive/model=ml_supcon
uv run python src/train.py contrastive/model=msc
uv run python src/train.py contrastive/model=mxclr
uv run python src/train.py contrastive/model=mxclr_rank
uv run python src/train.py contrastive/model=soft_jaccard
```

Switch classification strategy or loss:

```bash
uv run python src/train.py classification/strategy=finetune
uv run python src/train.py classification/loss=asymmetric
uv run python src/train.py classification/loss=zlpr
```

Inspect the resolved Hydra config:

```bash
uv run python src/train.py --cfg job --resolve
```

## Metrics And Logging

The classification stage logs the following epoch metrics for validation and test:

- `classification/val/f1_macro`
- `classification/val/f1_micro`
- `classification/val/hamming_loss`
- `classification/val/map`
- `classification/test/f1_macro`
- `classification/test/f1_micro`
- `classification/test/hamming_loss`
- `classification/test/map`

When the W&B logger is enabled, the run records Hydra configs after interpolation resolution, plus stable comparison aliases. During classification test, sigmoid scores and targets are saved as an artifact so test metrics can be recomputed from the artifact alone.

## Quality Checks

Run Python quality checks through uv.

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

`mypy` checks `src`, `tests`, and `scripts`.

Tests:

```bash
uv run pytest
uv run pytest -m "not slow"
```

Coverage:

```bash
uv run pytest --cov=src --cov-report=term-missing --cov-report=xml
```

Coverage output is written to `tmp/.coverage` and `tmp/coverage.xml`.

Property-based tests with Hypothesis:

```bash
uv run pytest tests/property
```

Manual Markdown structural formatting:

```bash
uv run pre-commit run mdformat --all-files --hook-stage manual
```

Standard pre-commit gate:

```bash
uv run pre-commit run -a
```

## Notes

- Use the repository-local `tmp/` directory for temporary files and validation logs.
- GPU-required validation must run on the local GPU machine.
- This is a research repository; do not add compatibility layers or temporary branches for old behavior.
- See `NOTICE` for attribution and external data notes.
