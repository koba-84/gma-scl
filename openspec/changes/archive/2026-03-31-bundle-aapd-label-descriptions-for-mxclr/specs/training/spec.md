## ADDED Requirements

### Requirement: MXCLR default initialization must not depend on untracked data files

The default MXCLR configuration MUST initialize successfully from the repository alone. When `dataset_name=aapd` and `label_description_path` is omitted, MXCLR MUST use bundled AAPD label descriptions shipped with the source tree instead of requiring a data file under `data/`.

#### Scenario: Resolve MXCLR default config without external label-description path

- **WHEN** 開発者が `PROJECT_ROOT=$(pwd) UV_CACHE_DIR=$PWD/tmp/uv-cache uv run python src/train.py --cfg job --resolve contrastive/model=mxclr` を実行する
- **THEN** `contrastive.model.loss_fn.label_description_path` は `null` として解決される
- **AND** `contrastive.model.loss_fn.dataset_name` は `aapd` として解決される

#### Scenario: Instantiate MXCLR default config from bundled AAPD descriptions

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr` を compose して model を instantiate する
- **THEN** `label_description_path` の FileNotFoundError は発生しない
- **AND** 初期化は source tree に bundled された AAPD label descriptions を用いて成功する

#### Scenario: Explicit missing label-description path still fails eagerly

- **WHEN** 開発者または coding agent が `dataset_name=aapd` かつ存在しない `label_description_path` を指定して MXCLR を初期化する
- **THEN** MXCLR は学習開始前に FileNotFoundError を送出する
