## Why

MXCLR と contrastive/classification 周辺に薄い helper や重複実装が残っており、責務境界が不明瞭です。label stats と aggregation の共有化を進めた直後なので、この段階で重複と分岐を整理して可読性を揃える必要があります。

## What Changes

- `src/models/loss/mxclr.py` の重複した label description loader を 1 つに統一する
- `src/models/loss/mcacr.py` の NPMI 読み込みを shared `label_stats` helper へ直接寄せる
- 未使用の `ContrastiveDataModule.get_train_base_dataset` を削除する
- `contrastive_module.py` と `finetune_module.py` の薄い batch-size / projection-dim helper を inline 化する
- MXCLR の `agg` 分岐を instantiate ベースの dispatch に置き換え、aggregator ごとの分岐を registry 側へ寄せる

## Capabilities

### New Capabilities

### Modified Capabilities

- training: MXCLR / MCACR / stage module の helper ownership と agg dispatch 契約を整理する

## Impact

- src/models/loss/mxclr.py
- src/models/loss/mcacr.py
- src/data/contrastive_datamodule.py
- src/models/contrastive_module.py
- src/models/finetune_module.py
- openspec/specs/training/spec.md
