## MODIFIED Requirements

### Requirement: Pre-commit is the mandatory local quality gate

Developers MUST run pre-commit hooks successfully before creating commits in this repository.

#### Scenario: Validate changes before commit

- **WHEN** 開発者が commit を作成する
- **THEN** `uv run pre-commit run -a` が成功している
- **AND** Python 変更では Ruff と mypy のフックが通過している

#### Scenario: Handle out-of-scope Markdown rewrites before task commit

- **WHEN** `uv run pre-commit run -a` によりタスク対象外の Markdown が自動修正される
- **THEN** 開発者または coding agent は当該 Markdown 差分を対象タスクの commit から分離しなければならない
- **AND** 対象外差分の扱い（別タスク化または別 change 化）を決定してから本来のタスク検証を継続する

## ADDED Requirements

### Requirement: Markdown auto-rewrite source attribution

The development workflow MUST identify which pre-commit hook rewrote Markdown files before deciding how to handle generated diffs.

#### Scenario: Attribute Markdown rewrite to specific hook

- **WHEN** `uv run pre-commit run -a` 実行後に Markdown 差分が発生する
- **THEN** 開発者または coding agent は Markdown を変更したフックを特定する
- **AND** 特定結果を根拠に差分分離または運用判断を行う
