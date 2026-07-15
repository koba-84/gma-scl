## MODIFIED Requirements

### Requirement: Layered test coverage from unit to integration

学習系の検証は、Loss 自己テストだけでなく、データコンポーネント層の軽量 unit/data-contract テストを MUST 含まなければならない。

#### Scenario: Define unit tests for data components

- **WHEN** 開発者が学習仕様のテスト節を確認する
- **THEN** `src/data/components/gcbs.py` が末尾自己テストで GCBS permutation と sampler の不変条件を検証する
- **AND** `src/data/components/dpp.py` が末尾自己テストで DPP sampler の初期化要件と入力制約を検証する
- **AND** `src/data/components/classification_dataset.py` が末尾自己テストで CSV 契約と異常入力を検証する
- **AND** `src/data/classification_datamodule.py` が末尾自己テストで dataloader 構築と `num_classes` 整合を検証する
- **AND** `src/data/contrastive_datamodule.py` が末尾自己テストで sampler 切替と初期化前エラーを検証する
- **AND** `src/models/components/mlp_head.py` が末尾自己テストで shape 契約を検証する

### Requirement: Standard execution commands for each test layer

各テスト階層は再現可能な標準コマンドを MUST 明示し、unit/data-contract 層を `not slow` 常時実行対象に含めなければならない。

#### Scenario: Execute fast checks before heavy integration

- **WHEN** 開発者が高速検証を実行する
- **THEN** `uv run python src/data/components/gcbs.py` で実行できる
- **AND** `uv run python src/data/components/dpp.py` で実行できる
- **AND** `uv run python src/data/components/classification_dataset.py` で実行できる
- **AND** `uv run python src/data/classification_datamodule.py` で実行できる
- **AND** `uv run python src/data/contrastive_datamodule.py` で実行できる
- **AND** `uv run python src/models/components/mlp_head.py` で実行できる
- **AND** 既存の学習統合テストは `slow` マーカー運用を維持する
