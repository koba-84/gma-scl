## Why

直近の W&B run では、比較列で使う `contrastive.model.loss_name` が空のまま残る一方、`contrastive/train/loss` と `contrastive/val/loss` は異なる x 軸定義に同時に一致して二重表示されている。実験比較の前提となる run metadata と metric 軸が安定していないため、欠損 run の backfill と今後の logging 契約の整理が必要である。

## What Changes

- 既存 run の `contrastive.model.loss_name` 欠損を backfill で補完する
- 学習時 logging でも `contrastive.model.loss_name` を比較用 alias として一貫して記録する
- contrastive metric の `define_metric` を整理し、`contrastive/train/loss` と `contrastive/val/loss` が単一の x 軸定義だけに一致するようにする
- W&B logger 既定の `trainer/global_step` 軸定義と競合しない stage metric 契約をテストで固定する

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: W&B config alias の補完契約と contrastive stage metric 軸の記録契約を更新する

## Impact

- 影響コード: `src/utils/logging_utils.py`, `src/models/contrastive_module.py`, `scripts/backfill_wandb_config.py`
- 影響テスト: W&B hyperparameter logging, contrastive metric 定義, backfill 補助コードの pytest
- 運用影響: 既存 run の backfill 実行、今後の run では W&B UI 上の重複系列が解消される
