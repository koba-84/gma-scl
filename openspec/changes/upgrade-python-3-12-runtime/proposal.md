## Why

現在のリポジトリは Python 3.10 前提の設定が `pyproject.toml`、CI、補助マニフェスト、README に分散しており、uv で再解決すると実際に使われる依存バージョンと宣言下限が乖離しています。研究実装として再現性を維持したまま Python 3.12 へ移行するには、実行系・依存下限・検証手順を一貫して更新し、変更理由を OpenSpec と lockfile に残す必要があります。

## What Changes

- `pyproject.toml` の Python 下限、Ruff target、mypy target を Python 3.12 に更新する。
- uv が Python 3.12 を選ぶよう `.python-version` を追加し、lockfile と worktree 環境を Python 3.12 で再生成する。
- Python 3.12 で実態に合わない依存下限を、PyTorch / Lightning / Transformers 系を中心に最小限だけ引き上げる。
- CI、補助マニフェスト、README の Python バージョン表記を Python 3.12 と整合するよう更新する。
- Python 3.12 環境で依存整合性、静的解析、pytest、import smoke、可能なら軽量な実行確認を行い、結果を記録する。

## Capabilities

### New Capabilities
- `python-runtime-baseline`: uv 管理下の Python 実行バージョン、依存下限、CI/文書表記を一貫して管理する。

### Modified Capabilities
- `dev-quality-tooling`: Ruff / mypy / pytest の検証手順を Python 3.12 ベースラインと整合させる。

## Impact

- 影響範囲: `pyproject.toml`, `uv.lock`, `.github/workflows/test.yml`, `.python-version`, `README.md`, `requirements.txt`, `environment.yaml`, `setup.py`, `openspec/project.md`
- 依存影響: Python 3.12 に不整合な下限の是正、および uv 再解決
- 検証影響: `uv run python -m pip check`, `uv run pytest -q`, `uv run ruff check .`, `uv run mypy`, import smoke、必要時の軽量実行確認
