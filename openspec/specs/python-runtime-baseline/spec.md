## Purpose

Define the repository-wide Python runtime baseline for uv-managed development and validation workflows.

## Requirements

### Requirement: Repository Python runtime baseline SHALL be 3.12 under uv

The repository MUST declare Python 3.12 as the canonical runtime baseline for local uv workflows and package metadata.

#### Scenario: Resolve project interpreter from repository metadata

- **WHEN** 開発者または coding agent がリポジトリ直下で uv を使って環境を作成または同期する
- **THEN** `pyproject.toml` の `requires-python` は Python 3.12 を下限として宣言している
- **AND** `.python-version` が Python 3.12 を指している

### Requirement: Python 3.12 baseline SHALL align runtime dependency floors

Dependencies that do not have a valid Python 3.12 baseline at their currently declared lower bounds MUST raise those lower bounds to the minimum supported series used by this repository, GPU-critical packages MUST resolve from a wheel source compatible with the validated local driver baseline, and Hugging Face runtime packages MUST remain within a validated major-version range when newer majors are known to break the local training path.

#### Scenario: Guard PyTorch family floor for Python 3.12

- **WHEN** 開発者が `pyproject.toml` の主要 runtime 依存下限を確認する
- **THEN** `torch` と `torchvision` の下限は Python 3.12 で成立する系列に更新されている
- **AND** `lightning` と `transformers` の下限は実際の Python 3.12 ベースラインと矛盾しない

#### Scenario: Resolve GPU-compatible PyTorch wheels for the validated driver baseline

- **WHEN** 開発者または coding agent が GPU 対応ローカルマシンで `uv lock` または `uv sync` を実行する
- **THEN** `torch` と `torchvision` は PyTorch 公式 wheel index のうち、検証済み driver baseline と互換な CUDA 系列から解決される
- **AND** PyPI 既定のより新しい CUDA 系列があっても、source pin により GPU 互換を優先する

#### Scenario: Keep transformers on a validated major series

- **WHEN** 開発者または coding agent が `pyproject.toml` と `uv.lock` の Hugging Face runtime 依存を更新する
- **THEN** `transformers` は `sentence-transformers` と既存 encoder forward で検証済みの 4 系 major range に制約されている
- **AND** 未検証の 5 系 major へ自動更新されない

### Requirement: Python 3.12 baseline SHALL align auxiliary manifests and CI

Repository-managed setup artifacts that publish or consume the Python baseline MUST stay aligned with the uv runtime baseline.

#### Scenario: Read CI and auxiliary setup manifests

- **WHEN** 開発者が GitHub Actions、補助マニフェスト、README のセットアップ手順を確認する
- **THEN** Python バージョン表記は Python 3.12 と整合している
- **AND** uv ベースの環境構築手順と矛盾しない
