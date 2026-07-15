## Why

classification 設定が model 名の下に学習戦略と loss を同居させており、分岐意図が読みにくい。研究実験での設定探索を簡潔化するため、strategy 軸と loss 軸を明示的に分離する。

## What Changes

- `configs/classification/model/` を廃止し、`configs/classification/strategy/` と `configs/classification/loss/` に再編する。
- `configs/classification/train.yaml` の defaults を `classification/strategy@model` と `classification/loss@model` の2軸合成へ変更する。
- 既存運用の `classification/model=...` 指定は廃止し、`classification/strategy=...` と `classification/loss=...` を使用する。

## Capabilities

### New Capabilities

- `classification-config-axis`: classification 設定の strategy/loss 2軸分離。

### Modified Capabilities

- `training`: classification stage の設定選択インターフェースを model 単軸から strategy/loss 2軸へ更新。

## Impact

- 影響コード: `configs/classification/train.yaml`, `configs/classification/strategy/*.yaml`, `configs/classification/loss/*.yaml`, `tests/`, `openspec/specs/training/spec.md`
- **BREAKING**: `classification/model=...` 指定は使えなくなる。
