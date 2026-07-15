## MODIFIED Requirements

### Requirement: Pre-commit hook consistency with Ruff and mypy

Pre-commit configuration MUST invoke Ruff hooks and mypy hook for Python checks so that local checks and manual checks stay consistent.

#### Scenario: Execute pre-commit on Python changes

- **WHEN** 開発者が Python ファイルを commit する
- **THEN** pre-commit で Ruff lint / Ruff format / mypy フックが実行される
- **AND** mypy フックは `uv run mypy` と同等スコープで検証される

### Requirement: Python quality command documentation

Repository documentation MUST publish Python quality commands including Ruff and mypy with current verification scope.

#### Scenario: Read quality-check section

- **WHEN** 開発者が README の品質チェック手順を確認する
- **THEN** `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy` が提示される
- **AND** mypy の対象スコープ（`src`, `tests`, `scripts`）が明記される
