## Why

tmp に持ち込んだ LossContrastiveMSC をこのリポジトリの標準学習経路で利用できず、実験比較に使えない。既存の contrastive loss と同じ設定運用で選択可能にして、再現可能に検証できる状態にする必要がある。

## What Changes

- src/models/loss/msc.py を追加し、公開クラス名 MSC を提供する。
- MSC は既存契約 loss_fn(z, labels) で動作し、必要な prototype はバッチ埋め込みから内部生成する。
- src/models/loss/__init__.py に公開シンボルを追加する。
- configs/contrastive/model/msc.yaml を追加し、Hydra 設定で選択可能にする。
- loss 自己テストと設定解決テストを追加し、最小動作を検証する。

## Capabilities

### New Capabilities

### Modified Capabilities

- training: contrastive loss の選択肢として MSC を追加し、Hydra 設定から解決できる要件を更新する。

## Impact

- 影響コード: src/models/loss/msc.py, src/models/loss/__init__.py, configs/contrastive/model/msc.yaml, openspec/specs/training/spec.md
- 既存 loss の forward 契約と train パイプラインは変更しない。
