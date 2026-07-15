## MODIFIED Requirements

### Requirement: MXCLR agg configs resolve documented family defaults

MXCLR configuration MUST keep common scalar hyperparameters in `configs/contrastive/model/mxclr.yaml`. Agg-family-specific settings MUST live under `configs/contrastive/model/agg/` and MUST be selected through Hydra defaults rather than a Python-side registry. The canonical family selector MUST be `contrastive.model.loss_fn.agg`, and `graph_builder` MUST NOT duplicate the same agg or transport strategy string when they are derivable from that selector.

#### Scenario: Resolve MXCLR default from agg config group

- **WHEN** 開発者が `PROJECT_ROOT=$(pwd) UV_CACHE_DIR=$PWD/tmp/uv-cache uv run python src/train.py --cfg job --resolve contrastive/model=mxclr` を実行する
- **THEN** `contrastive.model.loss_fn.agg` は `wmd` として解決される
- **AND** `contrastive.model.loss_fn.graph_builder._target_` は `src.models.loss.mxclr._build_mxclr_graph` として解決される
- **AND** `contrastive.model.loss_fn.graph_builder.agg` は解決対象に含まれない
- **AND** `contrastive.model.loss_fn.graph_builder.strategy` は解決対象に含まれない

#### Scenario: Resolve distill_idf_chamfer through agg config group override

- **WHEN** 開発者が `PROJECT_ROOT=$(pwd) uv run python src/train.py --cfg job --resolve contrastive/model=mxclr contrastive/model/agg@contrastive.model.loss_fn=distill_idf_chamfer` を実行する
- **THEN** `contrastive.model.loss_fn.agg` は `distill_idf_chamfer` として解決される
- **AND** `contrastive.model.loss_fn.graph_builder.use_label_idf` は `true` として解決される
- **AND** `contrastive.model.loss_fn.graph_builder.agg` は解決対象に含まれない
- **AND** `contrastive.model.loss_fn.graph_builder.strategy` は解決対象に含まれない
