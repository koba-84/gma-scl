## Why

tokenized pipeline へ移行した後も、encoder とバッチ契約に raw text 互換分岐が残っており、毎ミニバッチ処理のコードが複雑になっている。不要な分岐と互換経路を削除し、tokenized tensors 専用契約に一本化する。

## What Changes

- Encoder の raw text 入力分岐を削除し、`input_ids`/`attention_mask` 入力専用にする。
- classification/contrastive DataModule のバッチ契約を `(inputs, labels)` のみに簡素化する。
- Finetune/Contrastive モジュールの batch 型と処理分岐を更新する。
- 関連テストと設定を更新して、旧互換経路の不在を固定する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: tokenized 学習入力契約を最終化し、raw text 互換分岐を削除する。

## Impact

- 影響コード: `src/models/components/encoder.py`, `src/data/*datamodule.py`, `src/models/*module.py`, `tests/data_integration.py`
- **BREAKING**: text list を直接 model に渡す旧経路は利用不可になる
