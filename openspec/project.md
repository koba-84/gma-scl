# プロジェクト概要（実験コード）

## 目的

- 本リポジトリは実験コードである。
- 重要なのは「同じコミット + 同じHydra設定 + 同じseed」で同じ結果を再現できること。

## 実行環境（確定）

- uv: 0.7.9
- Python: 3.12.3
- 実行Python: ./.venv/bin/python3
- wandb: 0.25.1（uv環境に導入済み）
- GPU 用 PyTorch wheel: 公式 cu124 index から解決
- 実行は必ず `uv run ...` を用いる（システムPythonを踏まない）

## 設定管理（依存定義の正）

- 依存定義の正本は `pyproject.toml` と `uv.lock` とする。
- 依存追加・更新は必ず `uv add ...` で実施する。
- `requirements.txt` / `environment.yaml` は現行運用では使用しない（legacy 扱い）。

## 変更ルール（OpenSpecの使い方）

- 振る舞いが変わる変更（設定、データ、評価、モデル、サンプラ等）は OpenSpec change として
  仕様（spec）→計画（tasks）→実装 の形で残す。
- git commit/push の粒度は `openspec/specs/version-control.md` の規約に従う。
