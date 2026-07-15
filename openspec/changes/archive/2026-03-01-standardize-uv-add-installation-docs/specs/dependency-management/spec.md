## ADDED Requirements

### Requirement: Dependency definition source of truth

Project dependency definitions MUST be managed through pyproject.toml and uv.lock.

#### Scenario: Add runtime dependency

- **WHEN** 開発者が実行時依存を追加する
- **THEN** `uv add <package>` を使用して pyproject.toml と uv.lock を更新する

### Requirement: Installation flow must avoid pip and conda

Repository documentation MUST provide uv-based installation commands and MUST NOT instruct pip or conda usage for project dependency installation.

#### Scenario: Read installation section

- **WHEN** 開発者が README のインストール手順を参照する
- **THEN** 手順は uv に統一されている
- **AND** pip/conda による依存インストール手順は提示されない
