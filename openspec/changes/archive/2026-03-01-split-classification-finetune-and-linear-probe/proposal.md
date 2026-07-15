## Why

classification モデル設定が実態として linear probe なのにファイル名が finetune のため、設定選択時に意図を誤解しやすい。さらに、encoder を更新する finetune 設定を既定名で使いたい要件がある。

## What Changes

- 既存の `configs/classification/model/finetune.yaml` を `configs/classification/model/linear_probe.yaml` に改名する。
- 新規 `configs/classification/model/finetune.yaml` を追加し、既存設定を踏襲しつつ `encoder_freeze: false` とする。
- `configs/classification/train.yaml` の既定 model を finetune（非 freeze）として維持し、`classification/model=linear_probe` で freeze 構成を選択可能にする。

## Capabilities

### New Capabilities

- classification-model-presets: classification モデル設定で linear probe と finetune を明示的に選択できる。

### Modified Capabilities

- training: classification ステージの model 設定の既定挙動と選択肢を更新する。

## Impact

- 影響コード: `configs/classification/model/finetune.yaml`, `configs/classification/model/linear_probe.yaml`
- 影響設定: `configs/classification/train.yaml`（既定解決の確認対象）
- 運用影響: `classification/model=linear_probe` と `classification/model=finetune` を目的別に使い分け可能になる。
