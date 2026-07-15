## Why

現在の学習経路はエンコーダ内部で毎バッチ文字列をトークナイズしており、CPU前処理が学習スループットを制限している。Hugging Face Datasets を用いた事前トークナイズとキャッシュを標準化し、同一設定で再現可能な高速な入力パイプラインに置き換える。

## What Changes

- 学習データ読み込みを CSV 直読み中心から Hugging Face Datasets 中心に変更する。
- train/dev/test を batched map で事前トークナイズし、ディスクキャッシュを再利用する。
- エンコーダと学習モジュールを tokenized batch（input_ids/attention_mask/labels）入力へ変更する。
- contrastive/classification の DataModule を tokenized batch を返す実装へ統一する。
- **BREAKING**: 文字列バッチ前提の学習入力契約を廃止し、トークン化済みバッチ契約へ移行する。

## Capabilities

### New Capabilities

- `hf-datasets-tokenized-training-input`: Hugging Face Datasets の事前トークナイズとキャッシュ再利用を学習入力の標準経路として提供する。

### Modified Capabilities

- `training`: 学習時の入力契約を text list から tokenized tensor batch へ変更し、DataModule/Model 間のインターフェースを更新する。

## Impact

- 影響コード: `src/data/classification_datamodule.py`, `src/data/contrastive_datamodule.py`, `src/models/components/encoder.py`, `src/models/contrastive_module.py`, `src/models/finetune_module.py`
- 新規コード: `src/data/components/hf_tokenized_dataset.py`（予定）
- 依存関係: `datasets` の追加
- 影響設定: `configs/classification/data/*.yaml`, `configs/contrastive/data/*.yaml`
