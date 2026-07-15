## MODIFIED Requirements

### Requirement: CSV-based datasets must share the AAPD file contract

CSV-based multi-label datasets prepared for the training pipeline MUST provide `train.csv`, `dev.csv`, and `test.csv` files whose header starts with `abstract` followed by label columns, and whose label values are numeric binary floats compatible with AAPD (`0.0` or `1.0`). Dataset configs for such datasets MUST be selectable through Hydra for both contrastive and classification stages when the corresponding CSV files exist.

#### Scenario: WoS preprocessing emits AAPD-compatible splits

- **WHEN** `uv run python data/wos/preprocess.py` is executed
- **THEN** it writes `data/wos/train.csv`, `data/wos/dev.csv`, and `data/wos/test.csv`
- **AND** each file header starts with `abstract`
- **AND** label columns are numeric strings in deterministic order
- **AND** each row encodes the existing WoS document labels as `0.0`/`1.0` values

#### Scenario: Resolve Reuters-21578 data configs

- **WHEN** 開発者または coding agent が `data=reuters21578` を指定して train config を compose する
- **THEN** `contrastive.data.dataset_name` と `classification.data.dataset_name` は `reuters21578` として解決される
- **AND** `classification.data.num_classes` は Reuters-21578 CSV ヘッダのラベル列数と一致する `90` として解決される

#### Scenario: Resolve UK-LEX data configs

- **WHEN** 開発者または coding agent が `data=uklex` を指定して train config を compose する
- **THEN** `contrastive.data.dataset_name` と `classification.data.dataset_name` は `uklex` として解決される
- **AND** `classification.data.num_classes` は UK-LEX CSV ヘッダのラベル列数と一致する `69` として解決される
