## MODIFIED Requirements

### Requirement: MXCLR agg configs resolve documented family defaults

MXCLR configuration MUST keep common scalar hyperparameters in `configs/contrastive/model/mxclr.yaml`. Agg-family-specific settings MUST live under `configs/contrastive/model/agg/` and MUST be selected through Hydra defaults rather than a Python-side registry. Each agg config MUST instantiate a concrete graph implementation directly from `src/models/loss/agg/`, and MXCLR runtime code MUST NOT keep those concrete implementations in the top-level loss module. The default MXCLR config MUST point `label_description_path` to the existing AAPD label description file `data/aapd/label_descriptions.json`.

#### Scenario: Resolve MXCLR default from agg config group

- **WHEN** 開発者が `PROJECT_ROOT=$(pwd) UV_CACHE_DIR=$PWD/tmp/uv-cache uv run python src/train.py --cfg job --resolve contrastive/model=mxclr` を実行する
- **THEN** `contrastive.model.loss_fn.agg._target_` は `src.models.loss.agg.wmd.WmdGraph` として解決される
- **AND** `contrastive.model.loss_fn.gamma` は `0.0` として解決される
- **AND** `contrastive.model.loss_fn.label_description_path` は `data/aapd/label_descriptions.json` を参照する
- **AND** `contrastive.model.loss_fn.graph_builder` は解決対象に含まれない
- **AND** `src/models/loss/mxclr.py` は concrete agg 実装 class を持たない

#### Scenario: Instantiate MXCLR default config with bundled label descriptions

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr` を compose して model を instantiate する
- **THEN** `label_description_path` の FileNotFoundError は発生しない

#### Scenario: Resolve distill_chamfer with sinkhorn centering defaults

- **WHEN** 開発者が `PROJECT_ROOT=$(pwd) uv run python src/train.py --cfg job --resolve contrastive/model=mxclr contrastive/model/agg@contrastive.model.loss_fn=distill_chamfer` を実行する
- **THEN** `contrastive.model.loss_fn.agg.centering` は `sinkhorn_knopp` として解決される
- **AND** `contrastive.model.loss_fn.agg.sinkhorn_knopp_n_iters` は `3` として解決される
- **AND** `contrastive.model.loss_fn.agg.lambda_koleo` は `0.1` として解決される

#### Scenario: Resolve distill_idf_chamfer with sinkhorn centering defaults

- **WHEN** 開発者が `PROJECT_ROOT=$(pwd) uv run python src/train.py --cfg job --resolve contrastive/model=mxclr contrastive/model/agg@contrastive.model.loss_fn=distill_idf_chamfer` を実行する
- **THEN** `contrastive.model.loss_fn.agg.centering` は `sinkhorn_knopp` として解決される
- **AND** `contrastive.model.loss_fn.agg.sinkhorn_knopp_n_iters` は `3` として解決される
- **AND** `contrastive.model.loss_fn.agg.lambda_koleo` は `0.1` として解決される
