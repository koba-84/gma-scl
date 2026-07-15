## Why

MXCLR の transport 系 agg は現在すべて sinkhorn 実装に固定されています。それにもかかわらず `transport_optimization` という設定と引数が `mxclr.py`、agg config、transport helper 契約に残っており、切り替え可能であるかのような誤読を招きます。

## What Changes

- MXCLR と transport helper から `transport_optimization` を削除する
- transport 系 agg config から同名キーを削除し、sinkhorn 固定を実装側の契約として扱う
- training spec の MXCLR agg config 要件と transport helper 契約を現実の実装に合わせて更新する

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: MXCLR transport agg は sinkhorn 固定の契約に整理される

## Impact

- `src/models/loss/mxclr.py`
- `src/models/loss/components/transport.py`
- `configs/contrastive/model/agg/wmd.yaml`
- `configs/contrastive/model/agg/wrd.yaml`
- `configs/contrastive/model/agg/uot.yaml`
- `openspec/specs/training/spec.md`
