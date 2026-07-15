## Why

MXCLR の agg 実装は `graph_builder` に共通 builder 関数を置き、`agg` を code 側で解釈して処理を分けています。loss 側の instantiate ベース構成と比べると、agg 側だけ selector 文字列と共通 builder に依存していて一貫していません。

## What Changes

- 共通 builder 関数をやめ、agg config group が concrete graph 実装を直接 instantiate する
- `mxclr.py` から agg/family/policy の selector helper と総称 builder を削除する
- `agg` は可読性用の設定値として残すが、実行分岐には使わない
- MXCLR の tests と training spec を concrete 実装 instantiate 契約へ同期する

## Capabilities

### Modified Capabilities

- `training`: MXCLR agg config group は concrete graph 実装を直接選択する

## Impact

- `src/models/loss/mxclr.py`
- `configs/contrastive/model/mxclr.yaml`
- `configs/contrastive/model/agg/*.yaml`
- `tests/property_based.py`
- `tests/test_contrastive_losses.py`
- `openspec/specs/training/spec.md`
