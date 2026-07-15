## Why

contrastive 学習の既定 loss が ml_supcon になっており、base loss を基準にした比較実験を行うたびに明示 override が必要になっている。加えて contrastive epoch 数の比較実験を定型化できる hparams_search 設定がなく、再現実験の運用コストが高い。

## What Changes

- contrastive ステージのデフォルト model を ml_supcon から base に変更する。
- `configs/contrastive/train_ml_supcon.yaml` を削除し、loss 切替は `contrastive/model=...` 指定に統一する。
- contrastive epoch を 1, 5, 10, 20 で sweep できる hparams_search 設定を追加する。
- epoch sweep 設定では classification の既定設定（train/test=true）を維持し、下流評価まで実行する。
- OpenSpec の training 仕様に上記運用ルールを反映する。

## Capabilities

### New Capabilities

- contrastive-epoch-sweep: contrastive 学習の epoch 数を hparams_search でグリッド探索できる。

### Modified Capabilities

- training: contrastive デフォルト model と hparams_search 運用要件を更新する。

## Impact

- 影響コード: configs/contrastive/train.yaml, configs/contrastive/train_ml_supcon.yaml, configs/hparams_search/\*.yaml
- 影響仕様: openspec/specs/training.md
- 実験運用影響: 既定実行の loss が base へ切り替わる。
