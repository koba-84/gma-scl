## MODIFIED Requirements

### Requirement: MXCLR agg configs resolve documented family defaults

MXCLR configuration MUST keep common scalar hyperparameters in `configs/contrastive/model/mxclr.yaml`. Agg-family-specific settings MUST live under `configs/contrastive/model/agg/` and MUST be selected through Hydra defaults rather than a Python-side registry. Each agg config MUST instantiate a concrete graph implementation directly from `src/models/loss/agg/`, and MXCLR runtime code MUST NOT keep those concrete implementations in the top-level loss module. The default MXCLR config MUST resolve label descriptions from `data_dir` and `dataset_name` without exposing a separate `label_description_path` config key.

#### Scenario: Resolve MXCLR default from agg config group

- **WHEN** 開発者が `PROJECT_ROOT=$(pwd) UV_CACHE_DIR=$PWD/tmp/uv-cache uv run python src/train.py --cfg job --resolve contrastive/model=mxclr` を実行する
- **THEN** `contrastive.model.loss_fn.agg._target_` は `src.models.loss.agg.wmd.WmdGraph` として解決される
- **AND** `contrastive.model.loss_fn.gamma` は `0.0` として解決される
- **AND** `contrastive.model.loss_fn.data_dir` は `${contrastive.data.data_dir}` から解決される
- **AND** `contrastive.model.loss_fn.dataset_name` は `${contrastive.data.dataset_name}` から解決される
- **AND** `contrastive.model.loss_fn.label_description_path` は解決対象に含まれない
- **AND** `contrastive.model.loss_fn.graph_builder` は解決対象に含まれない
- **AND** `src/models/loss/mxclr.py` は concrete agg 実装 class を持たない

### Requirement: MXCLR default initialization must resolve dataset-scoped label descriptions

The default MXCLR configuration MUST initialize by reading `<data_dir>/<dataset_name>/label_descriptions.json`. MXCLR MUST NOT require a separate label-description path argument. If the dataset-scoped JSON is missing, MXCLR MUST fail eagerly before training starts.

#### Scenario: Instantiate MXCLR default config from tracked AAPD descriptions

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr` を compose して model を instantiate する
- **THEN** `data/aapd/label_descriptions.json` を用いて初期化に成功する

#### Scenario: Instantiate MXCLR with custom dataset descriptions

- **WHEN** 開発者または coding agent が `data_dir=<tmp_root>` `dataset_name=<custom_dataset>` かつ `<tmp_root>/<custom_dataset>/label_descriptions.json` を用意して MXCLR を初期化する
- **THEN** MXCLR は dataset 名に依存した追加制約なしで初期化に成功する

#### Scenario: Missing dataset-scoped descriptions fail eagerly

- **WHEN** 開発者または coding agent が `<data_dir>/<dataset_name>/label_descriptions.json` が存在しない状態で MXCLR を初期化する
- **THEN** MXCLR は学習開始前に FileNotFoundError を送出する
