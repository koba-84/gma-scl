## ADDED Requirements

### Requirement: Ruff naming rules must be part of mandatory quality gate
The mandatory quality gate MUST include Ruff pep8-naming validation for Python naming consistency.

#### Scenario: Enforce naming checks during pre-commit
- **WHEN** 開発者または coding agent が `uv run pre-commit run -a` を実行する
- **THEN** Ruff lint は pep8-naming (`N`) ルールを含めて実行される
- **AND** 命名違反がある場合は commit をブロックする

### Requirement: Naming validation command guidance must be documented
Repository documentation MUST provide an explicit command for naming-rule validation.

#### Scenario: Read naming check command in documentation
- **WHEN** 開発者が README の品質チェック手順を確認する
- **THEN** `uv run ruff check . --select N` が命名規約確認コマンドとして提示される
