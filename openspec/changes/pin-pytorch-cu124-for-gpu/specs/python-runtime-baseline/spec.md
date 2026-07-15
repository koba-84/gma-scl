## MODIFIED Requirements

### Requirement: Python 3.12 baseline SHALL align runtime dependency floors

Dependencies that do not have a valid Python 3.12 baseline at their currently declared lower bounds MUST raise those lower bounds to the minimum supported series used by this repository, and GPU-critical packages MUST resolve from a wheel source compatible with the validated local driver baseline.

#### Scenario: Guard PyTorch family floor for Python 3.12

- **WHEN** 開発者が `pyproject.toml` の主要 runtime 依存下限を確認する
- **THEN** `torch` と `torchvision` の下限は Python 3.12 で成立する系列に更新されている
- **AND** `lightning` と `transformers` の下限は実際の Python 3.12 ベースラインと矛盾しない

#### Scenario: Resolve GPU-compatible PyTorch wheels for the validated driver baseline

- **WHEN** 開発者または coding agent が GPU 対応ローカルマシンで `uv lock` または `uv sync` を実行する
- **THEN** `torch` と `torchvision` は PyTorch 公式 wheel index のうち、検証済み driver baseline と互換な CUDA 系列から解決される
- **AND** PyPI 既定のより新しい CUDA 系列があっても、source pin により GPU 互換を優先する
