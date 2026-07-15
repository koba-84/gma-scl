## ADDED Requirements

### Requirement: Classification model presets for probe and finetune

The training configuration SHALL provide two classification model presets: `linear_probe` and `finetune`.
`linear_probe` MUST set `encoder_freeze: true`, and `finetune` MUST set `encoder_freeze: false`.

#### Scenario: Select linear probe preset

- **WHEN** 開発者が `classification/model=linear_probe` を指定して設定を解決する
- **THEN** classification model の `encoder_freeze` は `true` でなければならない

#### Scenario: Use default finetune preset

- **WHEN** 開発者が `configs/classification/train.yaml` を既定のまま解決する
- **THEN** classification model は `finetune` を参照し
- **AND** `encoder_freeze` は `false` でなければならない
