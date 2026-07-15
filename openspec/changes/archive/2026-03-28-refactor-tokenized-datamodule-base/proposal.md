## Why

`build_or_load_tokenized_splits` が CSV schema 推定、tokenize、cache、load、bundle 組み立てまでを 1 つで握っており、datamodule の責務境界が読みにくい。Lightning hook に寄せた shared base datamodule へ再配置し、classification / contrastive の差分だけを残す。

## What Changes

- tokenized CSV の prepare/setup/cache load を shared base datamodule に集約する。
- `build_or_load_tokenized_splits` を廃止し、cache materialize と cached split load を private helper 群に分解する。
- classification / contrastive datamodule は sampler や num_classes 検証などの stage 固有差分だけを持つ。

## Capabilities

### New Capabilities

### Modified Capabilities

- `tokenized-datamodule-layout`: tokenized CSV datamodule の共有実装は Lightning hook ベースの shared base class に集約し、monolithic free function に依存しない

## Impact

- Affected code: `src/data/components/hf_tokenized_dataset.py`, `src/data/classification_datamodule.py`, `src/data/contrastive_datamodule.py`
- APIs: datamodule の外部 config 形は維持し、内部共有実装のみ変更
- Dependencies: 追加依存なし
