## Why

contrastive 学習の epoch 設定が通常実行と探索設定で不整合になっており、再現実験時の条件統一が崩れている。既定仕様を 80 epoch に固定し、実行条件の解釈を一意にする必要がある。

## What Changes

- contrastive 学習の既定 epoch を 80 に固定する。
- `configs/contrastive/train.yaml` の `contrastive.trainer.max_epochs` を 80 に更新する。
- training 仕様から epoch sweep 前提を除去し、contrastive epoch 固定ルールを明記する。
- hparams_search の `contrastive_epoch` は固定値 80 を前提とした再現用設定として整合を取る。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- training: contrastive 学習の epoch 運用要件を「80 固定」へ変更する。

## Impact

- 影響コード: configs/contrastive/train.yaml, configs/hparams_search/contrastive_epoch.yaml
- 影響仕様: openspec/specs/training/spec.md
- 実験運用影響: contrastive 学習条件が常に 80 epoch となり、実行ごとの差異を排除する。
