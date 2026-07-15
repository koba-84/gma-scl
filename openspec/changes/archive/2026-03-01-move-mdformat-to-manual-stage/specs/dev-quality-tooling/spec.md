## MODIFIED Requirements

### Requirement: Markdown rewrite attribution in pre-commit workflow

The development workflow MUST identify which pre-commit hook rewrote Markdown files before deciding how to handle generated diffs.

#### Scenario: Attribute rewrite source when Markdown diff appears

- **WHEN** `uv run pre-commit run -a` 実行後に Markdown 差分が発生する
- **THEN** 開発者または coding agent は `trailing-whitespace` `end-of-file-fixer` のいずれが差分を生成したか特定する
- **AND** `mdformat` は commit 時自動実行対象外であることを前提に運用判断を行う

### Requirement: Python quality command documentation

Repository documentation MUST publish Python quality commands including Ruff and mypy with current verification scope.

#### Scenario: Read quality-check section

- **WHEN** 開発者が README の品質チェック手順を確認する
- **THEN** `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy` が提示される
- **AND** mypy の対象スコープ（`src`, `tests`, `scripts`）が明記される

## ADDED Requirements

### Requirement: Manual Markdown formatting command guidance

Repository documentation MUST publish the manual mdformat execution command so Markdown structural formatting is reproducible outside commit-time hooks.

#### Scenario: Run mdformat manually for Markdown cleanup

- **WHEN** 開発者が Markdown 構文整形を実行する
- **THEN** `uv run pre-commit run mdformat --all-files --hook-stage manual` が案内される
- **AND** commit 時 `uv run pre-commit run -a` とは別運用であることが明記される
