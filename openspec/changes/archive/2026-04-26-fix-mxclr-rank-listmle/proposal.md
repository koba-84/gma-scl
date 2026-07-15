## Why

`mxclr_rank` は旧 ranking loss として ListMLE を使うべきだが、現状は `mxclr_kendall` と同じ differentiable Kendall tau 実装になっている。両者を同時に比較できるように、公開名ごとの ranking objective を分離する必要がある。

## What Changes

- `mxclr_rank` の ranking 項を ListMLE に戻す。
- `mxclr_rank` から Kendall 専用の `kendall_k` 公開引数を削除する。
- `mxclr_kendall` は differentiable Kendall tau のまま維持する。
- tests と training specs を更新し、`mxclr_rank` と `mxclr_kendall` の ranking objective の違いを検証する。

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: MXCLRRank は ListMLE、MXCLRKendall は differentiable Kendall tau を使う契約へ修正する。

## Impact

- 影響コード: `src/models/loss/mxclr_rank.py`, `configs/contrastive/model/mxclr_rank.yaml`, `tests/losses/test_mxclr_rank_loss.py`, `tests/test_configs.py`
- 影響仕様: `openspec/specs/training.md`, `openspec/specs/training/spec.md`
- 依存関係の追加はない。
