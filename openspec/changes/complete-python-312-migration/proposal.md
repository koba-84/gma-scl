## Why

リポジトリ全体として Python 3.12 へ移行した前提で運用されている一方、依存制約、lockfile、CI、補助環境定義、README、OpenSpec の実行環境文書には Python 3.10 が残っています。この不整合により、ローカル実行と CI の解釈が分岐し、再現性と保守性を損なっています。

## What Changes

- リポジトリ共通の Python 実行基準を 3.12 に更新し、OpenSpec で明文化する。
- `pyproject.toml` の `requires-python`、Ruff、mypy 設定を 3.12 基準へ更新する。
- `uv.lock` を Python 3.12 で再生成し、lockfile の `requires-python` と解決結果を 3.12 基準へ更新する。
- GitHub Actions のテスト workflow と補助 `environment.yaml` を 3.12 基準へ更新する。
- README と OpenSpec project 文書の Python 記載を 3.12 に揃える。

## Capabilities

### New Capabilities

- `python-runtime-baseline`: リポジトリの依存解決、CI、補助環境、文書が共通の Python 3.12 実行基準に従うことを定義する。

### Modified Capabilities

- `dev-quality-tooling`: 品質ツール設定は Python 3.12 の構文・型検査基準と一致する。

## Impact

- 影響仕様: 新規 `openspec/specs/python-runtime-baseline/spec.md`, `openspec/specs/dev-quality-tooling/spec.md`
- 影響コード: `pyproject.toml`, `uv.lock`, `.github/workflows/test.yml`, `environment.yaml`, `README.md`, `openspec/project.md`
- CI 影響: GitHub Actions のテスト job が Python 3.12 で統一される
