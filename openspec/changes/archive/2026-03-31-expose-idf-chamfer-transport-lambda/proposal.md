## Why

`idf_chamfer` は実装上 `transport_lambda` を受け取れる一方、Hydra config 側にキーが無いため通常 override ができません。結果として `contrastive_epoch` の sweeper 設定や手動 override が struct error で失敗します。

## What Changes

- `configs/contrastive/model/agg/idf_chamfer.yaml` に `transport_lambda: 5e-1` を追加する。
- `idf_chamfer` が Hydra override で `transport_lambda` を受け付ける要件を training spec に追加する。

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: MXCLR の `idf_chamfer` agg config が `transport_lambda` override を受け付けるようにする

## Impact

- 影響コード: `configs/contrastive/model/agg/idf_chamfer.yaml`
- 影響 spec: `openspec/specs/training/spec.md`
