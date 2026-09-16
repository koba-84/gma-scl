# GMA-SCL

AACL-IJCNLP 2026 Findings

Research code for GMA-SCL, a multi-label supervised contrastive learning implementation.
The repository provides a two-stage pipeline: contrastive pretraining followed by
classification evaluation. Experiments are configured with Hydra and run with PyTorch
Lightning.

## Features

- RoBERTa-based multi-label text classification
- Supervised contrastive learning and GMA-SCL objectives
- Datasets: AAPD, RCV1, Reuters-21578, and UK-LEX
- Single-dataset and mixed multi-dataset training profiles
- Reproducible Hydra configurations, seeded runs, and W&B/CSV logging

## Requirements

- Python 3.12
- `uv`
- CUDA-capable GPU for the full training workflow

Install the environment from `pyproject.toml` and `uv.lock`:

```bash
uv sync
```

## Data preparation

Datasets are not distributed with this repository. Prepare each dataset under
`data/<dataset_name>/` with the following files:

```text
data/
  aapd/
    train.csv
    dev.csv
    test.csv
    label_descriptions.json
  ...
```

Each CSV must contain an `abstract` column followed by binary label columns. GMA-SCL
also requires `label_descriptions.json` for the selected dataset. Dataset files and
their licenses remain the responsibility of the user; consult the original dataset
sources before redistribution.

## Quick start

Inspect the resolved default configuration without starting training:

```bash
uv run src/train.py --cfg job --resolve logger=csv
```

Run the default two-stage experiment with local CSV logging:

```bash
uv run src/train.py logger=csv
```

Run GMA-SCL explicitly:

```bash
uv run src/train.py contrastive/model=gma_scl logger=csv
```

The default workflow trains the contrastive stage first and then evaluates the
classification stage. Classification test evaluation selects the checkpoint with the
best validation macro-F1.

## Configuration

Select a dataset with a Hydra override:

```bash
uv run src/train.py data=rcv1 logger=csv
uv run src/train.py data=reuters21578 logger=csv
uv run src/train.py data=uklex logger=csv
```

Available contrastive model presets include:

```text
base, ml_supcon, mxclr, gma_scl, msc, soft_jaccard
```

For example:

```bash
uv run src/train.py contrastive/model=ml_supcon logger=csv
uv run src/train.py contrastive/model=mxclr logger=csv
```

The mixed multi-dataset profile uses one shared encoder and dataset-specific
classification heads:

```bash
uv run src/train.py \
  data=multi_dataset \
  contrastive/model=multi_dataset \
  classification/strategy@classification.model=multi_dataset \
  logger=csv
```

Override individual settings directly, for example:

```bash
uv run src/train.py \
  contrastive/model=gma_scl \
  contrastive.model.loss_fn.lambda_rank=0.5 \
  contrastive.trainer.max_epochs=1 \
  classification.trainer.max_epochs=1 \
  logger=csv
```

## Outputs and metrics

Hydra writes run outputs below `outputs/`. The classification stage records validation
and test macro/micro-F1, Hamming loss, and mean average precision. With W&B logging,
resolved configurations and prediction artifacts are also recorded.

For an online dashboard, replace `logger=csv` with `logger=wandb` and configure the
W&B credentials in the environment. The default W&B/Comet project name is `gma-scl`.

## Reproducibility and tests

The same Git commit, resolved Hydra configuration, dataset preparation, and seed are
needed to reproduce a result. Run the CPU-compatible checks with:

```bash
uv run pytest -m "not slow"
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

The complete execution check expects a local GPU:

```bash
scripts/test.sh
```

## Repository layout

```text
configs/       Hydra configurations for data, models, trainers, and loggers
src/           Training entrypoint, data modules, models, and losses
scripts/       Analysis and repository utility scripts
tests/         Unit, property, and integration tests
LICENSE        MIT License for the repository code
```

## License

The repository code is released under the [MIT License](LICENSE).
Datasets, pretrained models, and third-party components may have separate licenses and
are not relicensed by this notice.
