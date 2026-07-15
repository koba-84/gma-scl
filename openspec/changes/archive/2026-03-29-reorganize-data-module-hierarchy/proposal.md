## Why

`src/data/components` には低レベル部品と datamodule 基盤が混在しており、階層から責務を推測しづらい。dataset/sampler のような部品だけを `components` に残し、Lightning datamodule 基盤と tokenized cache orchestration は `src/data` 直下へ上げる。

## What Changes

- shared tokenized datamodule base を `src/data` 直下へ移す。
- tokenized cache orchestration module も `src/data` 直下へ移す。
- `components` には dataset wrapper / CSV dataset / sampler のみを残す。

## Capabilities

### New Capabilities

### Modified Capabilities

- `tokenized-datamodule-layout`: data hierarchy は datamodule-level module と low-level components を分離し、`components` に datamodule base を置かない

## Impact

- Affected code: `src/data/components/tokenized_csv_datamodule.py`, `src/data/components/tokenized_dataset_cache.py`, `src/data/classification_datamodule.py`, `src/data/contrastive_datamodule.py`
- APIs: import path のみ変更
- Dependencies: 追加依存なし
