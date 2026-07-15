## Why

classification stage の test metric は現状 run summary にしか残らず、sigmoid score と正解ラベルの対応を後から再利用できない。指標再計算や閾値再評価を run 後に再現可能にするため、test 時の予測ペアを W&B artifact として保存する契約が必要である。

## What Changes

- classification test で sigmoid 後 score と正解ラベルを全バッチ分収集し、再計算可能なファイルとして W&B artifact に保存する
- artifact には run 後に指標を再計算するための shape と label 次元情報を metadata として残す
- W&B logger が無い実行では追加保存を行わず、既存 test metric logging は維持する
- classification test artifact の保存契約を spec と pytest で固定する

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: classification test 出力の W&B artifact 保存契約を追加する

## Impact

- 影響コード:
  - `src/models/finetune_module.py`
- 影響テスト:
  - `tests/integration/data/test_data_integration.py`
  - `tests/integration/train/test_train_entrypoint.py`
- 影響仕様:
  - `openspec/specs/training/spec.md`
