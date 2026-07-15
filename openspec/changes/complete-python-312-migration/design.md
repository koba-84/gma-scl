## Context

`uv run python -V` はすでに Python 3.12.3 を返しており、実作業環境は 3.12 側へ移っています。一方で `pyproject.toml` の `requires-python` と開発ツール設定は 3.10 のままでした。さらに GitHub Actions と `environment.yaml` も 3.10 を前提としており、同一コミットでの再現条件が環境ごとに異なっていました。

## Goals

- 依存解決、静的検証、CI、補助環境、文書の Python 基準を 3.12 に統一する。
- lockfile を 3.12 で再生成し、`requires-python` と解決結果を 3.12 基準へ更新する。
- 既存の非 slow テストと品質ゲートが 3.12 で成立することを確認する。

## Non-Goals

- Python 3.10 互換の維持
- 依存ライブラリの不要なメジャー更新
- GPU 前提の学習設定自体の挙動変更

## Decisions

### 1. 実行基準は Python 3.12 に一本化する

後方互換レイヤーは追加せず、`pyproject.toml` と CI と補助環境はすべて 3.12 を基準に揃える。最小互換は `>=3.12` とし、研究コードの再現性文書では実測の 3.12 系実行値を示す。

### 2. lockfile は 3.12 で再生成する

`uv lock --python 3.12` を用いて lockfile を更新し、`requires-python` と解決結果を 3.12 基準へ置き換える。`uv.lock` には互換 upstream wheel 候補の metadata が残ることがあるため、判定対象はリポジトリが管理する Python 基準設定と実際の 3.12 解決結果とする。

### 3. 品質ツール設定も 3.12 基準へ更新する

Ruff の `target-version` と mypy の `python_version` を 3.12 へ更新し、CI 上の lint/type-check とローカル実行の解釈差をなくす。

### 4. 検証はローカルマシンで行う

品質ゲートと `pytest -m "not slow"` はローカルで実行する。GPU 前提の `scripts/test.sh` もローカルマシンで実行し、少なくとも Python 起動経路が 3.12 で揃っていることを確認する。
