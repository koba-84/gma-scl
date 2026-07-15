## ADDED Requirements

### Requirement: Planned expansion of property-based tests

The project MUST maintain explicit OpenSpec tasks for incremental expansion of Hypothesis-based property tests across prioritized pure functions.

#### Scenario: Track next property-based targets as tasks

- **WHEN** 開発者が property-based test の次対象を計画する
- **THEN** OpenSpec の tasks.md に対象関数ごとの task が定義される
- **AND** 各 task は不変条件または契約観点を明記する

### Requirement: Test file naming must follow training spec

Tests under `tests/` MUST avoid `test` in filenames and use feature-based names.

#### Scenario: Rename non-compliant pytest files

- **WHEN** tests 配下に `test` 語を含むファイル名が存在する
- **THEN** ファイル名は feature-based 名称（例: `property_based.py`, `task_wrapper.py`）へ改名される
- **AND** 実行コマンドと関連文書の参照パスが同期される
