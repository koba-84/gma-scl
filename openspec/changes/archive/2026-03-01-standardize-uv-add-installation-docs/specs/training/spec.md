## ADDED Requirements

### Requirement: Dependency updates in training workflow use uv add

Training workflow documentation MUST define dependency updates through uv add and MUST avoid pip/conda based dependency installation.

#### Scenario: Add training-related dependency

- **WHEN** 開発者が学習関連の依存を追加する
- **THEN** `uv add <package>` を使用する
- **AND** 開発補助用途の場合は `uv add --group dev <package>` を使用する
