## Why

MXCLR loss と contrastive module で埋め込み正規化の書き方が分散しており、同じ処理意図の追跡がしづらくなっています。あわせて classification datamodule の train/val/test 用データ取得が同一実装の重複になっているため、保守時の読みやすさを落としています。

## What Changes

- 正規化処理を torch.nn.functional.normalize に統一し、専用 helper の重複を除去する
- classification datamodule の train/val/test 向けデータ存在確認を 1 つの共通 helper に集約する
- 変更後の実装方針を OpenSpec の training capability に反映する

## Capabilities

### New Capabilities

### Modified Capabilities

- training: 学習関連モジュールの内部実装で正規化とデータ存在確認の共通化方針を明文化する

## Impact

- src/models/loss/mxclr.py
- src/models/contrastive_module.py
- src/data/classification_datamodule.py
- openspec/specs/training/spec.md
