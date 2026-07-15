## Why

`mxclr_rank` は現在 row-wise ListMLE を ranking 項として使っているが、順位相関を直接最適化する微分可能な Kendall τ を使いたい要件がある。`MXCLR + lambda_rank * kendall_loss` へ置換し、teacher/student の順位整合をより直接的に最適化できるようにする。

## What Changes

- `MXCLRRank` の ranking 項を ListMLE から differentiable Kendall τ loss に置換する。
- ranking loss 実装で teacher/student logits を row-wise 標準化したうえで pairwise Kendall 項を計算する。
- ranking 強度を制御する `k`（温度係数）を `MXCLRRank` と Hydra config で明示設定できるようにする。
- pytest と training spec を更新し、`mxclr_loss + lambda_rank * kendall_loss` の契約を検証する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: `mxclr_rank` の ranking 項を ListMLE から differentiable Kendall τ に変更し、`lambda_rank` と `k` で寄与を制御できるようにする

## Impact

- 影響コード: `src/models/loss/mxclr_rank.py`, `src/models/loss/components/` 配下の ranking helper, `configs/contrastive/model/mxclr_rank.yaml`, `tests/losses/test_mxclr_rank_loss.py`
- 影響仕様: `openspec/specs/training/spec.md`, `openspec/specs/training.md`
- 実験運用: `mxclr_rank` は ListMLE 前提ではなくなり、微分可能 Kendall τ を ranking 補助損失として使う
