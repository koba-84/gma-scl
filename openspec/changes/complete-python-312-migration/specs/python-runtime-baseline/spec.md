## ADDED Requirements

### Requirement: Repository Python baseline must be 3.12
Repository dependency metadata, lockfile resolution, CI runners, and auxiliary environment definitions MUST use Python 3.12 as the common baseline.

#### Scenario: Resolve dependencies for local development
- **WHEN** 開発者または coding agent が `uv sync` または `uv lock` を実行する
- **THEN** `pyproject.toml` と `uv.lock` は Python 3.12 を前提に解決される
- **AND** リポジトリが管理する Python 基準設定に Python 3.10 を残さない

#### Scenario: Run repository test workflow in CI
- **WHEN** GitHub Actions の test workflow が実行される
- **THEN** `actions/setup-python` は Python 3.12 をセットアップする
- **AND** `uv sync --frozen` と pytest 実行は同じ 3.12 基準で動作する

#### Scenario: Read auxiliary environment definition
- **WHEN** 開発者が `environment.yaml` や OpenSpec project 文書を参照する
- **THEN** Python 実行基準は 3.12 と記載されている
- **AND** README の Python 表記とも矛盾しない
