## ADDED Requirements

### Requirement: Autonomous commit must pass mandatory quality gate

Coding agents MUST pass mandatory local quality checks before creating autonomous commits for Python changes.

#### Scenario: Autonomous commit after successful pre-commit

- **WHEN** coding agent が Python 変更を含む commit を自律作成する
- **THEN** `uv run pre-commit run -a` は commit 作成前に成功している
- **AND** pre-commit 内の Ruff / mypy フックが通過している

#### Scenario: Autonomous commit blocked by quality failure

- **WHEN** `uv run pre-commit run -a` または mypy フックが失敗している
- **THEN** coding agent は commit を作成してはならない
- **AND** 失敗内容と未実行項目を報告する
