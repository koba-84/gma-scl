## Why

MXCLR の類似度集約は現在 mean に固定されており、MCACR 比較実験で過去方式との切り替え検証がしづらい。設定引数で集約方式を切り替えられるようにして、同一実装内で再現比較を可能にする。

## What Changes

- MXCLR に agg 引数を追加し、類似度集約方式を切り替え可能にする。
- similarity_graph で agg に応じた分岐を実装する。
- 不正な agg 指定時は初期化時に明示的な例外を送出する。
- MXCLR の設定ファイルと自己テストを agg 分岐対応に更新する。

## Capabilities

### New Capabilities

- `mxclr-aggregation-selection`: MXCLR が agg 引数で集約方式を選択できることを定義する。

### Modified Capabilities

- `training`: MXCLR の初期化・類似度集約契約に agg 指定と分岐可能性を追加する。

## Impact

- 影響コード: src/models/loss/mxclr.py, configs/contrastive/model/mxclr.yaml
- 影響仕様: openspec/specs/training/spec.md
- 影響検証: uv run python src/models/loss/mxclr.py
