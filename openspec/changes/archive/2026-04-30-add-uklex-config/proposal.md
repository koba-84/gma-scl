## Why

UK-LEX の前処理済み CSV と label metadata は `data/uklex/` に存在しますが、Hydra の data config group から選択できません。既存の tokenized datamodule は CSV 契約に従う dataset を `dataset_name` で読み込めるため、UK-LEX も contrastive と classification の両 stage から明示的に選択できる設定が必要です。

## What Changes

- `configs/data/uklex.yaml` を追加し、contrastive/classification の両 stage を uklex に切り替える
- `configs/contrastive/data/uklex.yaml` を追加する
- `configs/classification/data/uklex.yaml` を追加し、`num_classes` を 69 に固定する
- UK-LEX の config 解決を検証する

## Capabilities

### Modified Capabilities

- `tokenized-datamodule-layout`: CSV-based dataset config として uklex を Hydra から選択できるようにする

## Impact

- 影響範囲: Hydra data config と OpenSpec spec
- 実行影響: `data=uklex` と `classification/data=uklex` の設定解決が可能になる
- 非対象: データ前処理、モデル、損失、学習ロジック
