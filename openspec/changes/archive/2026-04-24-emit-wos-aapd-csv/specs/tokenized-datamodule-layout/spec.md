## MODIFIED Requirements

### Requirement: CSV-based datasets must share the AAPD file contract

CSV-based multi-label datasets prepared for the training pipeline MUST provide `train.csv`, `dev.csv`, and `test.csv` files whose header starts with `abstract` followed by label columns, and whose label values are numeric binary floats compatible with AAPD (`0.0` or `1.0`).

#### Scenario: WoS preprocessing emits AAPD-compatible splits

- **WHEN** `uv run python data/wos/preprocess.py` is executed
- **THEN** it writes `data/wos/train.csv`, `data/wos/dev.csv`, and `data/wos/test.csv`
- **AND** each file header starts with `abstract`
- **AND** label columns are numeric strings in deterministic order
- **AND** each row encodes the existing WoS document labels as `0.0`/`1.0` values
