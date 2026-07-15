## MODIFIED Requirements

### Requirement: Dependency updates must use uv add

Dependency updates for training workflows MUST be performed with `uv add` commands, and project documentation MUST NOT instruct dependency installation via pip or conda.

#### Scenario: Add runtime dependency for training

- **WHEN** 開発者が学習関連の実行時依存を追加する
- **THEN** `uv add <package>` を使用する

#### Scenario: Add non-runtime dependency for training

- **WHEN** 開発者が学習関連の開発依存または追加機能依存を追加する
- **THEN** `uv add --group dev <package>` を使用する

#### Scenario: Add Ruff as development dependency

- **WHEN** 開発者が Python 品質チェック基盤として Ruff を導入する
- **THEN** `uv add --group dev ruff` を使用する
