## 1. OpenSpec Artifact Preparation

- [x] 1.1 proposal.md に変更目的と影響範囲を記述する
- [x] 1.2 specs に gcbs-quantile-sweep-layout と training の要件差分を記述する
- [x] 1.3 design.md に実装方針とトレードオフを記述する

## 2. Hyperparameter Search Config Migration

- [x] 2.1 configs/hparams_search/gcbs_quantile_grid.yaml を削除する
- [x] 2.2 test1 から test4 を GCBS quantile 探索設定へ更新する
- [x] 2.3 変更後の設定を確認して不要参照がないことを検証する

## 3. Spec Sync

- [x] 3.1 main spec へ反映し、training 仕様の運用記述を更新する
