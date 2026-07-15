## MODIFIED Requirements

### Requirement: Layered test coverage from unit to integration

fast integration テストは DataModule/sampler 接続だけでなく、data quality・data schema 契約・reproducibility・stage 間 artifact 契約の観点を MUST 含まなければならない。

#### Scenario: Validate data quality and reproducibility in fast integration

- **WHEN** 開発者が fast integration テストを実行する
- **THEN** tiny データでラベル分布の簡易 skew 検証が行われる
- **AND** split 間の列不一致（schema 契約違反）を検知できる
- **AND** 固定 seed 条件で sampler 経路の再現性が検証される
- **AND** contrastive から classification への checkpoint 引き渡し契約を検証できる

### Requirement: Standard execution commands for each test layer

tests ディレクトリ配下の pytest テストファイル名は `test` 語を含まない命名を MUST 採用し、実行コマンドは新命名へ同期されなければならない。

#### Scenario: Collect and run renamed tests

- **WHEN** 開発者が `uv run pytest --collect-only -q` を実行する
- **THEN** tests 配下の機能名ベースファイル（例: `train.py`, `data_integration.py`）が収集される
- **AND** `uv run pytest -m "not slow" -q` で fast integration が実行できる
