## Why

`transformers>=4.34.0` のみを宣言した現状では、uv が `transformers 5.4.0` を解決し、ローカルの学習経路で Hugging Face 側の内部 `NameError` を引き起こしている。研究実装として同じ lockfile で安定再現できる状態に戻すため、`sentence-transformers 5.3.0` と整合する安定な 4 系列へ runtime を固定する必要がある。

## What Changes

- `pyproject.toml` の runtime 依存で `transformers` に 5 未満の上限を追加する。
- `uv.lock` を更新し、ローカル uv 環境の解決結果を 4 系へ揃える。
- `transformers` の import と最小 forward を再検証し、5 系で出ていた実行時エラーが発生しないことを確認する。
- Python runtime baseline spec に、Hugging Face 系 runtime が major upgrade で不安定化しない制約を明記する。

## Capabilities

### New Capabilities

### Modified Capabilities
- `python-runtime-baseline`: Python 3.12 baseline で Hugging Face runtime 依存が実運用で検証済みの major 系列に固定される要件を追加する

## Impact

- 影響範囲: `pyproject.toml`, `uv.lock`, `openspec/specs/python-runtime-baseline/spec.md`
- 依存影響: `transformers` を 5 未満へ制約し、`sentence-transformers` と整合する解決結果に固定
- 検証影響: `uv lock`, `uv sync`, `transformers` import smoke, encoder forward smoke
