## Why

MXCLR の既定 config が存在しない `data/aapd/arxiv_label_descriptions.json` を参照しており、`contrastive/model=mxclr` の instantiate が即時に失敗します。既定 config だけで正常に立ち上がる状態へ戻す必要があります。

## What Changes

- MXCLR config の `label_description_path` を実在する AAPD ラベル説明 JSON に修正する。
- `contrastive/model=mxclr` が既定 config のまま instantiate できる test を追加する。
- training spec の参照ファイル名を現行の実データに合わせて更新する。

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: MXCLR の既定 label description path 要件を実在ファイル名へ更新する

## Impact

- 影響コード: `configs/contrastive/model/mxclr.yaml`
- 影響テスト: `tests/configs.py`
- 影響 spec: `openspec/specs/training/spec.md`, `openspec/specs/training.md`
