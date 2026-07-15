## Why

contrastive 後の classification は現行の 100 epoch だと比較実験の周回コストが高く、運用上の既定値と乖離しています。あわせて contrastive_epoch の探索設定を MXCLR + IDF chamfer 系の再現条件に寄せ、参照するだけで同じ探索前提を共有できる状態にする必要があります。

## What Changes

- classification stage の既定 `max_epochs` を 100 から 40 に変更する。
- `configs/hparams_search/contrastive_epoch.yaml` を MXCLR 用の探索 preset に変更する。
- 同 sweep config で MXCLR loss の `gamma=2`、agg を `idf_chamfer`、NPMI 混合重みを `5e-1` として解決されるようにする。

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: classification の既定 epoch 上限と contrastive_epoch 探索 preset の要求を更新する

## Impact

- 影響ファイル: `configs/classification/train.yaml`, `configs/hparams_search/contrastive_epoch.yaml`
- 影響 spec: `openspec/specs/training/spec.md`
- 学習挙動への影響: classification の既定学習長、contrastive_epoch 探索時のモデル系統と MXCLR hyperparameter
