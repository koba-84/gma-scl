## MODIFIED Requirements

### Requirement: Default runtime acceleration settings

Training defaults MUST enable runtime acceleration features that are already supported by the repository implementation.

#### Scenario: Resolve default compile settings for both stages

- **WHEN** 開発者が `PROJECT_ROOT=$(pwd) uv run python src/train.py --cfg job --resolve` を実行する
- **THEN** `contrastive.model.compile` は `true` として解決される
- **AND** `classification.model.compile` は `true` として解決される

#### Scenario: Resolve default pinned-memory dataloaders for tokenized stages

- **WHEN** 開発者が `PROJECT_ROOT=$(pwd) uv run python src/train.py --cfg job --resolve` を実行する
- **THEN** `contrastive.data.pin_memory` は `true` として解決される
- **AND** `classification.data.pin_memory` は `true` として解決される
