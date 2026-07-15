## Why

現在の mypy 検証は `src/models` と `src/data` に限定されており、`src/utils`・`src/train.py`・`tests`・`scripts` の型不整合は実行時まで検出できない。研究コードの回帰を早期に防ぐため、mypy をリポジトリ全体の Python 実装へ段階拡張する必要がある。

## What Changes

- mypy の検証対象を `src/models`, `src/data` からリポジトリ内 Python 実装全体へ拡張する。
- `src/utils`, `src/train.py`, `tests`, `scripts` の型エラーを解消する。
- `pyproject.toml` の mypy 設定を「段階導入しやすく、Any 伝播を抑制する」方針へ更新する。
- pre-commit の mypy フックを全体検証前提へ更新し、ローカル検証と手動実行の整合を保つ。
- README の品質チェック手順に、全体 mypy 検証スコープを明記する。

## Capabilities

### New Capabilities

- `repo-wide-mypy-validation`: リポジトリ全体の Python コードを mypy で継続検証する運用要件を定義する。

### Modified Capabilities

- `dev-quality-tooling`: Ruff 中心の品質運用に mypy の全体検証を追加し、pre-commit と手動実行の整合要件を拡張する。

## Impact

- 影響ファイル: `pyproject.toml`, `.pre-commit-config.yaml`, `README.md`, `src/utils/*.py`, `src/train.py`, `src/data/*.py`, `tests/*.py`, `scripts/*.py`
- 依存: 追加ライブラリは不要（既存 `mypy` を利用）
- 開発フロー: commit 前/手動の型検証が一段厳格化され、型エラーを早期検出できる
