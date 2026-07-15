## Why

linear_probe 実験で contrastive/classification の学習率探索範囲が固定化されておらず、再現実験時に比較条件がぶれやすい。
contrastive と classification の探索候補を明示して、実験条件を統一する。

## What Changes

- `configs/hparams_search/contrastive_epoch.yaml` の sweep 値を更新し、contrastive 側の学習率候補を `5e-5,1e-4` に統一する。
- 同ファイルの classification 側学習率候補を `1e-3,5e-4` に統一する。
- 学習仕様ドキュメントへ上記の linear_probe 学習率探索条件を反映する。

## Capabilities

### New Capabilities
- なし

### Modified Capabilities
- `training`: linear_probe における contrastive/classification の learning rate sweep 仕様を更新する

## Impact

- 影響コード: `configs/hparams_search/contrastive_epoch.yaml`
- 影響仕様: `openspec/specs/training/spec.md`, `openspec/specs/training.md`
- 実験運用: linear_probe の再現実験で使用する学習率組み合わせが明確化される
