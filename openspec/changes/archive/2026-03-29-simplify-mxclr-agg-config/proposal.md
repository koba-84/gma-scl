## Why

現在の MXCLR agg config では、`loss_fn.agg` と `loss_fn.graph_builder.agg` が常に同じ値を持ち、transport family では `graph_builder.strategy` も同じ文字列を重ねて持っています。family selector が複数箇所に分散しており、設定が冗長です。

## What Changes

- MXCLR は `agg` を唯一の family selector として扱う
- `graph_builder` から `agg` と `strategy` を削除し、必要な差分は family 固有フラグだけに絞る
- `mxclr.yaml` と agg config group を再編し、graph builder の共通 target は base config に置く
- MXCLR の pytest と training spec を新しい config 契約に同期する

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: MXCLR agg config は単一 selector と最小フラグで表現される

## Impact

- `src/models/loss/mxclr.py`
- `configs/contrastive/model/mxclr.yaml`
- `configs/contrastive/model/agg/*.yaml`
- `tests/property_based.py`
- `tests/test_contrastive_losses.py`
- `openspec/specs/training/spec.md`
