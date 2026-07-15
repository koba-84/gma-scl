## ADDED Requirements

### Requirement: Fixed contrastive training epoch

The training configuration MUST fix `contrastive.trainer.max_epochs` to 80 in the default contrastive stage settings.

#### Scenario: Resolve default contrastive epoch

- **WHEN** 開発者が `uv run python src/train.py --cfg job --resolve` を実行する
- **THEN** 解決済み設定の `contrastive.trainer.max_epochs` は `80` である

## MODIFIED Requirements

### Requirement: Stage defaults in train config

The train configuration SHALL include both contrastive and classification stages by default.

#### Scenario: Resolve default train config

- **WHEN** 開発者が `uv run python src/train.py --cfg job --resolve` を実行する
- **THEN** 設定に contrastive と classification の両方が含まれる
- **AND** classification.model の損失設定を解決してインスタンス化できる
- **AND** contrastive ステージは固定 epoch (`contrastive.trainer.max_epochs=80`) を満たす
