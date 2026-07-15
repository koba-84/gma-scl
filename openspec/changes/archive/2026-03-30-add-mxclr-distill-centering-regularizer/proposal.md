## Why

MXCLR の `distill_chamfer` / `distill_idf_chamfer` は現在、Sentence-BERT 埋め込みから各ラベル平均を引く centering に固定されています。この実装では、DINOv2 系 distillation で使われる Sinkhorn-Knopp ベースの assignment centering を比較できず、また distill 系 agg で特徴分散を維持する正則化も持っていません。

## What Changes

- distill 系 MXCLR agg に `centering` 設定を追加し、`mean` と `sinkhorn_knopp` を切り替え可能にする
- `sinkhorn_knopp` centering は `n_iters=3` で動作し、DINOv2 と同型の反復正規化を用いる
- distill 系 MXCLR agg に KoLeo regularizer を追加し、`lambda_koleo=0.1`、適用前 L2 normalize を既定動作とする
- training spec を更新し、distill 系 agg config が上記 hyperparameter を明示解決する契約へ揃える

## Capabilities

### New Capabilities

- `training`: MXCLR distill 系 agg は Sinkhorn-Knopp centering と KoLeo regularizer を設定で有効化できる

### Modified Capabilities

- `training`: MXCLR distill 系 agg は平均引き centering 固定ではなくなる

## Impact

- `src/models/loss/agg/distill_chamfer.py`
- `src/models/loss/agg/distill_idf_chamfer.py`
- `src/models/loss/mxclr.py`
- `configs/contrastive/model/agg/distill_chamfer.yaml`
- `configs/contrastive/model/agg/distill_idf_chamfer.yaml`
- `tests/property_based.py`
- `tests/test_contrastive_losses.py`
- `openspec/specs/training/spec.md`
