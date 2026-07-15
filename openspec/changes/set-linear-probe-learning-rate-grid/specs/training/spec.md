## ADDED Requirements

### Requirement: Linear probe learning-rate sweep grid for contrastive epoch search
`configs/hparams_search/contrastive_epoch.yaml` MUST define the linear_probe learning-rate sweep grid with exactly two candidates for each stage: contrastive `5e-5,1e-4` and classification `1e-3,5e-4`.

#### Scenario: Resolve contrastive and classification lr candidates from sweep config
- **WHEN** 開発者が `uv run python src/train.py -m hparams_search=contrastive_epoch --cfg job --resolve` を実行する
- **THEN** `contrastive.model.optimizer.lr` は `5e-5,1e-4` を候補として解決される
- **AND** `classification.model.optimizer.lr` は `1e-3,5e-4` を候補として解決される

#### Scenario: Keep scientific notation in learning-rate grid
- **WHEN** 開発者または coding agent が当該 sweep 設定を更新する
- **THEN** learning rate は指数表記（例: `1e-3`）で記述される
- **AND** 小数表記（例: `0.001`）は使用しない
