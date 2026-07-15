## MODIFIED Requirements

### Requirement: Ruff naming rules must be part of mandatory quality gate

The mandatory quality gate MUST include Ruff pep8-naming validation for Python naming consistency.

#### Scenario: Enforce naming checks during pre-commit

- **WHEN** 開発者または coding agent が `uv run pre-commit run -a` を実行する
- **THEN** Ruff lint は pep8-naming (`N`) ルールを含めて実行される
- **AND** 命名違反がある場合は commit をブロックする
- **AND** 命名ルール向けの custom ignore-names を既定で持たない
