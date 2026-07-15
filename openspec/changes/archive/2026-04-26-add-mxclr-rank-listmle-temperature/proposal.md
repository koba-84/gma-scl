## Why

`MXCLRRank` の ListMLE ranking 項は現在 `instance_temperature` を共有しているが、contrastive soft-target loss 側の温度と ranking loss 側の鋭さは別々に調整したい。再現性のため、ListMLE 専用温度を config に明示する必要がある。

## What Changes

- `MXCLRRank` に ListMLE ranking 項専用の `rank_temperature` を追加する。
- `configs/contrastive/model/mxclr_rank.yaml` に `rank_temperature` を明示する。
- `rank_temperature` は正値のみ許可し、`instance_temperature` とは独立して `student_scores` の scaling に使う。
- tests と training specs を更新し、MXCLR 本体温度と ListMLE 温度が分離されることを検証する。

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: MXCLRRank の ListMLE ranking 項が専用 `rank_temperature` を使う契約へ変更する。

## Impact

- 影響コード: `src/models/loss/mxclr_rank.py`, `configs/contrastive/model/mxclr_rank.yaml`, `tests/losses/test_mxclr_rank_loss.py`, `tests/test_configs.py`
- 影響仕様: `openspec/specs/training.md`, `openspec/specs/training/spec.md`
- 依存関係の追加はない。
