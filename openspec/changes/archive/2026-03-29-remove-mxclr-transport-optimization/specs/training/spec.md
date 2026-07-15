## MODIFIED Requirements

### Requirement: MXCLR agg configs resolve documented family defaults

MXCLR configuration MUST keep common scalar hyperparameters in `configs/contrastive/model/mxclr.yaml`. Agg-family-specific graph builder settings MUST live under `configs/contrastive/model/agg/` and MUST be selected through Hydra defaults rather than a Python-side registry. Transport-based agg configs MUST NOT expose redundant backend-selection keys when the implementation is fixed to sinkhorn-family solvers.

#### Scenario: Resolve MXCLR default from agg config group

- **WHEN** 開発者が `PROJECT_ROOT=$(pwd) UV_CACHE_DIR=$PWD/tmp/uv-cache uv run python src/train.py --cfg job --resolve contrastive/model=mxclr` を実行する
- **THEN** `contrastive.model.loss_fn.agg` は `wmd` として解決される
- **AND** `contrastive.model.loss_fn.graph_builder` は agg group 由来の partial callable config として解決される
- **AND** `contrastive.model.loss_fn.transport_optimization` は解決対象に含まれない

#### Scenario: Resolve distill_idf_chamfer through agg config group override

- **WHEN** 開発者が `PROJECT_ROOT=$(pwd) uv run python src/train.py --cfg job --resolve contrastive/model=mxclr contrastive/model/agg@contrastive.model.loss_fn=distill_idf_chamfer` を実行する
- **THEN** `contrastive.model.loss_fn.agg` は `distill_idf_chamfer` として解決される
- **AND** `contrastive.model.loss_fn.graph_builder.use_label_idf` は `true` として解決される
- **AND** `contrastive.model.loss_fn.transport_optimization` は解決対象に含まれない

### Requirement: MXCLR transport helper contract must define shared inputs and outputs

The public helper in `src/models/loss/components/transport.py` MUST expose one canonical module contract: it accepts `labels_bin: [N, L]`, `cost_matrix: [L, L]`, `label_weights: [L]`, and an explicit transport strategy selector, and it returns a pairwise distance matrix `[N, N]`. Public helper names MUST NOT be split by transport family when the input/output contract is otherwise identical. The helper MUST NOT expose an extra backend-selection argument when the backend is fixed by implementation policy.
