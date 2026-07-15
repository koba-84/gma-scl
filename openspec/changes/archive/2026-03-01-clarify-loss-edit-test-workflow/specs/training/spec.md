## ADDED Requirements

### Requirement: 既存 Loss 編集時の最低テスト手順

`src/models/loss` 配下の既存 Loss 実装を編集した場合、開発者は MUST 対象ファイル自己テストと設定解決テストを実施しなければならない。

#### Scenario: 既存 MCACR 実装を編集した場合

- **WHEN** 開発者が `src/models/loss/mcacr.py` を編集する
- **THEN** `uv run python src/models/loss/mcacr.py` と `uv run pytest tests/test_configs.py -q` を実施する

### Requirement: 既存 Loss 編集時の影響ベース追加テスト

既存 Loss 編集で入出力契約または実行経路条件が変わる場合、開発者は MUST 下記の対応する統合テストを追加実施しなければならない。

#### Scenario: 初期化契約を変更する

- **WHEN** `__init__` の引数、必須 config キー、初期化時に読む入力、初期化時例外条件を変更する
- **THEN** `tests/test_configs.py` と `tests/test_train.py` を追加実施する

#### Scenario: 学習経路に影響する Loss 編集

- **WHEN** `forward` の入力契約または出力契約を変更する
- **THEN** `tests/test_train.py` と `tests/test_eval.py` を追加実施する

#### Scenario: sweep または実機確認が必要な Loss 編集

- **WHEN** Hydra sweep 参照キーを変更する
- **THEN** `tests/test_sweeps.py` を追加実施する

#### Scenario: CUDA または precision 依存処理を変更する

- **WHEN** 編集内容が CUDA 分岐または precision 依存処理を変更する
- **THEN** `scripts/test.sh` を追加実施する
