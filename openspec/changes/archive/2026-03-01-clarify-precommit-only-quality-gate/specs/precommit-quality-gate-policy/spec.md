## ADDED Requirements

### Requirement: Pre-commit is the mandatory local quality gate

Developers MUST run pre-commit hooks successfully before creating commits in this repository.

#### Scenario: Validate changes before commit

- **WHEN** 開発者が commit を作成する
- **THEN** `uv run pre-commit run -a` が成功している
- **AND** Python 変更では Ruff と mypy のフックが通過している
