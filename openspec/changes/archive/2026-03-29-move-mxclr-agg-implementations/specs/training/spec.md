## MODIFIED Requirements

### Requirement: MXCLR agg configs resolve documented family defaults

MXCLR configuration MUST keep common scalar hyperparameters in `configs/contrastive/model/mxclr.yaml`. Agg-family-specific settings MUST live under `configs/contrastive/model/agg/` and MUST be selected through Hydra defaults rather than a Python-side registry. Each agg config MUST instantiate a concrete graph implementation directly from `src/models/loss/agg/`, and MXCLR runtime code MUST NOT keep those concrete implementations in the top-level loss module.

#### Scenario: Resolve MXCLR default from agg config group

- **WHEN** 開発者が `PROJECT_ROOT=$(pwd) UV_CACHE_DIR=$PWD/tmp/uv-cache uv run python src/train.py --cfg job --resolve contrastive/model=mxclr` を実行する
- **THEN** `contrastive.model.loss_fn.agg._target_` は `src.models.loss.agg.wmd.WmdGraph` として解決される
- **AND** `contrastive.model.loss_fn.graph_builder` は解決対象に含まれない
- **AND** `src/models/loss/mxclr.py` は concrete agg 実装 class を持たない
