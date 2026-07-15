## Why

MCACR では負例項にラベル類似度由来の重みを使っているが、距離ベース重みのみの寄与を切り分けて検証したい。既存実装に同条件の派生 loss がないため、設定で切り替え可能な実装を追加する。

## What Changes

- MCACR の負例項からラベル由来重みを除外し、距離ベース重みのみを使う新しい loss クラス `MCACR_WONEG` を追加する。
- 新クラスを公開 API（loss パッケージ）に追加する。
- Hydra 設定で新クラスを選択できるよう、contrastive model 設定を追加する。
- インスタンス化と forward の最小検証テストを追加する。

## Capabilities

### New Capabilities

- `mcacr-woneg-loss`: MCACR の負例重みを距離ベースのみに固定した contrastive loss を設定から選択できる。

### Modified Capabilities

- `training`: contrastive loss の選択肢として `MCACR_WONEG` を追加し、Hydra 設定から解決できる要件を追加する。

## Impact

- 影響コード: `src/models/loss/mcacr.py`, `src/models/loss/__init__.py`, `configs/contrastive/model/*.yaml`, `tests/*`
- 既存 `MCACR` の挙動は変更しない（新規クラス追加のみ）。
