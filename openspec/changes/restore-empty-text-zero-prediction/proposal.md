## Why

tokenized-only 契約への移行時に、空テキスト行の test 予測を 0 にする既存挙動が失われた。評価互換性を維持するため、空テキスト判定に基づく予測ゼロ化を復元する。

## What Changes

- 前処理で空テキスト判定フラグを生成し、バッチ入力へ含める。
- classification の test_step で空テキスト行の予測を 0 に強制する処理を復元する。
- no-text batch 契約は維持し、text payload を戻さない。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: classification test 時の空テキスト行予測を 0 化する挙動を復元する。

## Impact

- 影響コード: `src/data/components/hf_tokenized_dataset.py`, `src/data/classification_datamodule.py`, `src/models/finetune_module.py`, `tests/data_integration.py`
- 互換性: バッチ契約 `(inputs, labels)` は維持しつつ、inputs に空テキストフラグを追加
