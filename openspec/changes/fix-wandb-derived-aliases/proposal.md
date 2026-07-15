## Why

W&B の比較列で参照したい `contrastive.model.loss_name` `contrastive.model.loss_fn.agg` `contrastive.model.loss_fn.tau_s` が、実験時 logging と backfill で一貫して補完されていない。特に contrastive loss 名は `_target_` の module 名から機械的に導出できるので、明示 map を減らして実装追加時のメンテナンスコストを下げたい。

## What Changes

- contrastive loss 名は `_target_` の module 名から導出する
- MXCLR 系の `agg` alias を `loss_fn.agg._target_` から導出する
- MXCLR_PROTO の `tau_s` alias は `tau_s_schedule.start` から導出する
- logging と backfill で同じ導出 helper を使う

## Impact

- 影響コード: `src/utils/logging_utils.py`, `src/utils/wandb_config_aliases.py`, `scripts/backfill_wandb_config.py`
- 影響テスト: W&B alias 導出と hyperparameter logging の pytest
