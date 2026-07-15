## Why

`hf_tokenized_dataset.py` に tokenized row wrapper と cache/materialize 実装が同居しており、module 名と責務がずれている。dataset wrapper と tokenized cache helper を分離して、名前と実装を一致させる。

## What Changes

- `hf_tokenized_dataset.py` は `TokenizedDatasetBundle` と `TokenizedTorchDataset` のみを持つ。
- tokenized cache の materialize/load helper を別 module へ移す。
- shared base datamodule の import を新 module に切り替える。

## Capabilities

### New Capabilities

### Modified Capabilities

- `tokenized-datamodule-layout`: tokenized dataset wrapper module は cache orchestration を持たず、cache helper は別 module に分離される

## Impact

- Affected code: `src/data/components/hf_tokenized_dataset.py`, `src/data/components/tokenized_csv_datamodule.py`
- APIs: shared base が参照する cache helper の import 先
- Dependencies: 追加依存なし
