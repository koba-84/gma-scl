## MODIFIED Requirements

### Requirement: Layered test coverage from unit to integration

学習系の検証は、実装ファイル内自己テストに加えて、DataModule と sampler の fast integration テストを MUST 含まなければならない。

#### Scenario: Validate datamodule and sampler integration paths

- **WHEN** 開発者が `tests/data_integration.py` を実行する
- **THEN** `ClassificationDataModule` の `prepare_data` / `setup` / dataloader 連携が検証される
- **AND** `ContrastiveDataModule` の `sampler_type=shuffle/gcbs/dpp` 経路が検証される
- **AND** `dpp` で埋め込み未設定時の失敗と設定後成功が検証される

### Requirement: Standard execution commands for each test layer

fast integration テストは `not slow` 常時実行対象として再現可能なコマンドを MUST 提供しなければならない。

#### Scenario: Run fast integration checks in local and CI

- **WHEN** 開発者が fast integration を実行する
- **THEN** `uv run pytest tests/data_integration.py -q` で実行できる
- **AND** `uv run pytest -m "not slow" tests/data_integration.py -q` で実行できる
