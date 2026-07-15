## Why

W&B の config 画面で Hydra の `${...}` 補間が未解決のまま残っており、実際に使われた値を run 画面から直接確認できません。再現性の観点では、W&B 上でも解決済み設定がそのまま読める必要があります。

## What Changes

- W&B へ送る hyperparameters を補間解決済みの plain container に変換する。
- stage ごとの hyperparameter logging で `${...}` 文字列が残らないことをテストで保証する。
- training spec に W&B config 解決要件を追加する。

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: W&B に保存する config の解決方法に関する要件を追加する

## Impact

- 影響コード: `src/utils/logging_utils.py`
- 影響テスト: `tests/`
- 影響 spec: `openspec/specs/training/spec.md`
