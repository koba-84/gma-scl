## Why

実験の反復速度を上げるため、既定設定と tokenized dataset の取り扱いを見直したい。現状は GPU 転送の既定値が保守的で、tokenized split から各 sample を取り出すたびに tensor を再生成しており、長い contrastive/classification 実験で無駄な CPU 側オーバーヘッドが発生する。

## What Changes

- contrastive / classification の tokenized datamodule 既定値で `pin_memory` を有効化する。
- tokenized Hugging Face split を torch format で保持し、`__getitem__` ごとの tensor 再生成をなくす。
- contrastive / classification の model config 既定値で `compile` を有効化する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: 高速化のための既定 runtime 設定として compile 有効化と GPU 転送向け pin_memory 有効化を定義する。
- `tokenized-datamodule-layout`: tokenized dataset が各 sample 取得時に tensor を再構築せず、再利用可能な torch 形式で split を提供するよう要求を拡張する。

## Impact

- Affected code: `configs/contrastive/data/*.yaml`, `configs/classification/data/*.yaml`, `configs/contrastive/model/default.yaml`, `configs/classification/strategy/*.yaml`, `src/data/components/hf_tokenized_dataset.py`
- Runtime systems: dataloader host-to-device transfer path, torch compile path, Hugging Face dataset access path
- Validation: config resolve, tokenized dataset unit tests, targeted pytest
