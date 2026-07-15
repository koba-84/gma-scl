## Why

直近 2 回の MXCLR 実験では、追加差分が `contrastive.model.loss_fn.gamma` 中心だったにもかかわらず、W&B の config には stage ごとの実効設定が一部空欄または不完全なまま残りました。再現性のためには、Hydra の最終解決値だけでなく、stage 実行時に merge された trainer/model 設定も W&B 上でそのまま確認できる必要があります。

## What Changes

- stage 実行時に実際に使う `contrastive` / `classification` の merged config を W&B へ記録する。
- W&B 比較列で参照しやすいよう、主要 config leaf を dot-path の flat key としても記録する。
- stage override を含む W&B hyperparameter logging のテストを追加し、空欄や未反映を再発防止する。
- 直近 2 実験の欠損 config を W&B API で補完するメンテナンス手順または補助コードを追加する。

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: W&B へ保存する stage config を stage 実効値ベースで記録する要件に更新する

## Impact

- 影響コード: `src/train.py`, `src/utils/logging_utils.py`
- 影響テスト: `tests/test_logging_utils.py`
- 影響運用: W&B project `multi-label-supcon` の既存 run backfill
- 影響 spec: `openspec/specs/training/spec.md`
