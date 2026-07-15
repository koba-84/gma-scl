## ADDED Requirements

### Requirement: Classification stage default epoch budget

The default classification stage configuration MUST cap `classification.trainer.max_epochs` at `40`.

#### Scenario: Resolve classification default max epochs

- **WHEN** 開発者が `uv run python src/train.py --cfg job --resolve` を実行する
- **THEN** `classification.trainer.max_epochs` は `40` として解決される

## MODIFIED Requirements

### Requirement: Linear probe learning-rate sweep grid for contrastive epoch search

`configs/hparams_search/contrastive_epoch.yaml` MUST define the linear_probe learning-rate sweep grid with exactly two candidates for each stage: contrastive `5e-5,1e-4` and classification `1e-3,5e-4`. The same sweep config MUST resolve the MXCLR preset with `contrastive/model: mxclr`, `contrastive/model/agg@contrastive.model.loss_fn: idf_chamfer`, `contrastive.model.loss_fn.agg.transport_lambda: 5e-1`, and `contrastive.model.loss_fn.gamma: 2`.

#### Scenario: Resolve contrastive and classification lr candidates from sweep config

- **WHEN** 開発者が `uv run python src/train.py hparams_search=contrastive_epoch --cfg hydra -p hydra.sweeper.params --resolve` を実行する
- **THEN** `contrastive.model.optimizer.lr` は `5e-5,1e-4` を候補として解決される
- **AND** `classification.model.optimizer.lr` は `1e-3,5e-4` を候補として解決される

#### Scenario: Resolve MXCLR preset from sweep config

- **WHEN** 開発者が `uv run python src/train.py hparams_search=contrastive_epoch --cfg hydra -p hydra.sweeper.params --resolve` を実行する
- **THEN** `contrastive/model` は `mxclr` として解決される
- **AND** `contrastive/model/agg@contrastive.model.loss_fn` は `idf_chamfer` として解決される
- **AND** `contrastive.model.loss_fn.agg.transport_lambda` は `5e-1` として解決される
- **AND** `contrastive.model.loss_fn.gamma` は `2` として解決される

#### Scenario: Keep scientific notation in learning-rate grid

- **WHEN** 開発者または coding agent が当該 sweep 設定を更新する
- **THEN** learning rate は指数表記（例: `1e-3`）で記述される
- **AND** 小数表記（例: `0.001`）は使用しない

#### Scenario: Keep descending order in multi-value learning-rate candidates

- **WHEN** 開発者または coding agent が learning-rate 候補を複数値で列挙する
- **THEN** 候補は数値の降順（高い値から低い値）で記述される
- **AND** 例として `1e-4,5e-5` の順序を使用する
