## Why

直近 2 実験では nested config の leaf は補完された一方で、W&B 比較列で参照していた `contrastive.model.loss_name` などの派生 alias が空欄のままでした。現行 config から一意に導ける loss alias も継続して記録しないと、run 間比較の再現性が落ちます。

## What Changes

- W&B logging で `contrastive.model.loss_name` と `classification.model.loss_name` を派生 alias として記録する。
- W&B backfill 補助コードでも同じ alias を補完できるようにする。
- 直近 2 run に loss alias を backfill する。

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: W&B 比較で使う派生 loss alias を継続して記録する要件を追加する

## Impact

- 影響コード: `src/utils/logging_utils.py`, `scripts/backfill_wandb_config.py`
- 影響テスト: `tests/test_logging_utils.py`
- 影響運用: W&B runs `vn1tc1hq`, `zoov78x6`
- 影響 spec: `openspec/specs/training/spec.md`
