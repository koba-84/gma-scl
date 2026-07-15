## ADDED Requirements

### Requirement: Loss implementation self-test in source files

`src/models/loss` 配下の各 Loss 実装ファイルは、ファイル末尾で直接実行可能な簡易単体テストを MUST 提供しなければならない。

#### Scenario: Run self-test from loss source file

- **WHEN** 開発者が `uv run python src/models/loss/<loss_file>.py` を実行する
- **THEN** その Loss の自己テストが実行され、終了コード 0 で完了する

### Requirement: Minimum assertions for loss self-test

各 Loss 自己テストは、最低限次の検証を MUST 含まなければならない: 1) 正常入力で有限スカラーを返すこと 2) 主要な入力不正に対して想定例外を送出すること。

#### Scenario: Validate normal and invalid paths

- **WHEN** 開発者が Loss 自己テストコードを確認する
- **THEN** 有限スカラーの確認アサーションが存在する
- **AND** 入力バリデーション失敗の確認アサーションが少なくとも 1 つ存在する

### Requirement: Temporary artifact handling for loss self-test

Loss 自己テストで一時ファイルが必要な場合、保存先は `multi-label/tmp` を MUST 使用し、テスト終了時に削除しなければならない。

#### Scenario: Self-test uses temporary NPMI or auxiliary files

- **WHEN** NPMI などの一時ファイルを使う Loss 自己テストを実行する
- **THEN** 一時ファイルは `multi-label/tmp` 配下に作成される
- **AND** テスト終了時にクリーンアップされる

### Requirement: Layered test coverage from unit to integration

学習系の検証は、Loss 単体自己テストから pytest 統合テスト、実機 GPU 実行までの階層で MUST 定義されなければならない。

#### Scenario: Define test layers and targets

- **WHEN** 開発者が学習仕様のテスト節を確認する
- **THEN** Loss 自己テスト（`src/models/loss/*.py`）が単体レイヤとして定義される
- **AND** pytest の統合レイヤとして `tests/test_configs.py`, `tests/test_train.py`, `tests/test_eval.py`, `tests/test_sweeps.py` が定義される
- **AND** 実機 GPU 統合レイヤとして `scripts/test.sh` が定義される

### Requirement: Standard execution commands for each test layer

各テスト階層は、再現可能な標準コマンドを MUST 明示しなければならない。

#### Scenario: Execute tests by documented commands

- **WHEN** 開発者が仕様に従ってテストを実行する
- **THEN** Loss 単体は `uv run python src/models/loss/<loss_file>.py` で実行できる
- **AND** pytest 統合は `uv run pytest <target> -q` で実行できる
- **AND** 実機 GPU 統合はローカルマシンで `scripts/test.sh` を実行する手順が示される
