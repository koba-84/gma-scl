## MODIFIED Requirements

### Requirement: MXCLR agg configs resolve documented family defaults

MXCLR configuration MUST keep common scalar hyperparameters in `configs/contrastive/model/mxclr.yaml`. Agg-family-specific settings MUST live under `configs/contrastive/model/agg/` and MUST be selected through Hydra defaults rather than a Python-side registry. Each agg config MUST instantiate a concrete graph implementation directly, and MXCLR runtime code MUST NOT dispatch among agg families through a shared builder function.

#### Scenario: Resolve MXCLR default from agg config group

- **WHEN** 開発者が `PROJECT_ROOT=$(pwd) UV_CACHE_DIR=$PWD/tmp/uv-cache uv run python src/train.py --cfg job --resolve contrastive/model=mxclr` を実行する
- **THEN** `contrastive.model.loss_fn.agg` は `wmd` として解決される
- **AND** `contrastive.model.loss_fn.graph_builder._target_` は WMD 用の concrete graph 実装として解決される
- **AND** `contrastive.model.loss_fn.graph_builder.agg` は解決対象に含まれない
- **AND** `contrastive.model.loss_fn.graph_builder.strategy` は解決対象に含まれない
- **AND** `contrastive.model.loss_fn.graph_builder.matrix_kind` は解決対象に含まれない

#### Scenario: Resolve mean through agg config group

- **WHEN** 開発者が `PROJECT_ROOT=$(pwd) uv run python src/train.py --cfg job --resolve contrastive/model=mxclr contrastive/model/agg@contrastive.model.loss_fn=mean` を実行する
- **THEN** `contrastive.model.loss_fn.agg` は `mean` として解決される
- **AND** `contrastive.model.loss_fn.graph_builder._target_` は mean 用の concrete graph 実装として解決される
- **AND** `contrastive.model.loss_fn.graph_builder.strategy` は解決対象に含まれない
- **AND** `contrastive.model.loss_fn.graph_builder.matrix_kind` は解決対象に含まれない
