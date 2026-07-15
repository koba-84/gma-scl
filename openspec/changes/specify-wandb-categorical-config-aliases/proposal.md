## Why

W&B config の数値 leaf は比較しやすい一方、loss や MXCLR agg のような有限選択肢は structured config のどこに比較用名前を置くかが曖昧で、nested subtree を潰す alias も混在している。比較列として安定した配置を仕様化し、全選択肢を網羅するテストで固定する必要がある。

## What Changes

- implementation-backed な有限選択肢は `*_name` alias として stable leaf に記録する契約を追加する
- `contrastive.model.loss_fn.agg` を上書きする旧 alias を廃止し、subtree を保持したまま `contrastive.model.loss_fn.agg_name` を記録する
- support している contrastive loss、classification loss、MXCLR agg の全選択肢を網羅する pytest を追加する
- logging と backfill が同じ categorical alias 契約を共有するように更新する

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: W&B categorical config alias の配置と命名契約を更新する

## Impact

- 影響コード:
  - `src/utils/wandb_config_aliases.py`
  - `src/utils/logging_utils.py`
  - `scripts/backfill_wandb_config.py`
- 影響テスト:
  - `tests/test_wandb_config_aliases.py`
  - `tests/test_logging_utils.py`
  - `tests/test_backfill_wandb_config.py`
- 影響仕様:
  - `openspec/specs/training/spec.md`
