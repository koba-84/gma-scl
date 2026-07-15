## Why

既存の contrastive loss クラス名 `BaseMultiLabelContrastiveLoss` は用途に対して冗長で、設定ファイルやコードレビュー時の可読性を下げている。研究コードでは命名の簡潔さと一貫性が再現実験の運用効率に直結するため、命名を整理する。

## What Changes

- `BaseMultiLabelContrastiveLoss` を `Base` に改名する。
- `MultiLabelSupConLoss` を `MulSupCon` に改名する。
- loss エクスポートと Hydra 設定の参照先を新クラス名に更新する。
- 既存の暫定互換レイヤーは追加しない（BREAKING）。
- 既存 loss クラス（`MCACRLoss`）の命名を確認し、現状を記録する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: contrastive loss 実装の命名を `Base`, `MulSupCon`, `MCACR` の方針へ統一する要件へ更新する。

## Impact

- 影響コード: `src/models/loss/base.py`, `src/models/loss/ml_supcon.py`, `src/models/loss/__init__.py`, `configs/contrastive/model/base.yaml`, `configs/contrastive/model/ml_supcon.yaml`
- 間接影響: `from src.models.loss import BaseMultiLabelContrastiveLoss` の外部参照がある場合は破壊的変更となる。
