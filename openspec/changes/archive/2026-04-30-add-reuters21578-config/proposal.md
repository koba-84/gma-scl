## Why

既存の hparams search config は `data: reuters21578` や `classification/data: reuters21578` を参照していますが、Hydra の data config group に reuters21578 が存在しないため設定解決が成立しません。ローカルの `data/reuters21578/train.csv` は 90 ラベルの CSV 契約に従っており、contrastive と classification の両 stage から選択できる設定が必要です。

## What Changes

- `configs/data/reuters21578.yaml` を追加し、contrastive/classification の両 stage を reuters21578 に切り替える
- `configs/contrastive/data/reuters21578.yaml` を追加する
- `configs/classification/data/reuters21578.yaml` を追加し、`num_classes` を 90 に固定する
- reuters21578 の config 解決を検証する

## Capabilities

### Modified Capabilities

- `tokenized-datamodule-layout`: CSV-based dataset config として reuters21578 を Hydra から選択できるようにする

## Impact

- 影響範囲: Hydra data config と OpenSpec spec
- 実行影響: `data=reuters21578` と `classification/data=reuters21578` の設定解決が可能になる
- 非対象: データ前処理、モデル、損失、学習ロジック
