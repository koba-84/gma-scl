## ADDED Requirements

### Requirement: Python quality tooling must target the declared runtime baseline
Ruff and mypy configuration MUST target the repository Python runtime baseline so local checks, CI, and dependency metadata use the same language level.

#### Scenario: Run Ruff and mypy under the repository baseline
- **WHEN** 開発者または coding agent が `uv run ruff check .` または `uv run mypy` を実行する
- **THEN** Ruff `target-version` は `py312` である
- **AND** mypy `python_version` は `3.12` である
- **AND** `pyproject.toml` の `requires-python` と矛盾しない
