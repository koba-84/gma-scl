## ADDED Requirements

### Requirement: Repository Python runtime baseline SHALL be 3.12 under uv

The repository MUST declare Python 3.12 as the canonical runtime baseline for local uv workflows and package metadata.

#### Scenario: Resolve project interpreter from repository metadata

- **WHEN** 開発者または coding agent がリポジトリ直下で uv を使って環境を作成または同期する
- **THEN** `pyproject.toml` の `requires-python` は Python 3.12 を下限として宣言している
- **AND** `.python-version` が Python 3.12 を指している

### Requirement: Python 3.12 baseline SHALL align runtime dependency floors

Dependencies that do not have a valid Python 3.12 baseline at their currently declared lower bounds MUST raise those lower bounds to the minimum supported series used by this repository.

#### Scenario: Guard PyTorch family floor for Python 3.12

- **WHEN** 開発者が `pyproject.toml` の主要 runtime 依存下限を確認する
- **THEN** `torch` と `torchvision` の下限は Python 3.12 で成立する系列に更新されている
- **AND** `lightning` と `transformers` の下限は実際の Python 3.12 ベースラインと矛盾しない

### Requirement: Python 3.12 baseline SHALL align auxiliary manifests and CI

Repository-managed setup artifacts that publish or consume the Python baseline MUST stay aligned with the uv runtime baseline.

#### Scenario: Read CI and auxiliary setup manifests

- **WHEN** 開発者が GitHub Actions、補助マニフェスト、README のセットアップ手順を確認する
- **THEN** Python バージョン表記は Python 3.12 と整合している
- **AND** uv ベースの環境構築手順と矛盾しない
