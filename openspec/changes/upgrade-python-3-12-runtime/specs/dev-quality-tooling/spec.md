## ADDED Requirements

### Requirement: Python quality configuration SHALL target the repository runtime baseline

Ruff and mypy configuration MUST target the same Python runtime baseline that the repository declares for uv execution.

#### Scenario: Read Python quality configuration after runtime baseline upgrade

- **WHEN** 開発者が `pyproject.toml` の Ruff と mypy 設定を確認する
- **THEN** Ruff の `target-version` は Python 3.12 を対象としている
- **AND** mypy の `python_version` は Python 3.12 を対象としている
