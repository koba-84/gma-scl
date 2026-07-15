### Requirement: MXCLR must auto-load agg-required label statistics

MXCLR MUST inspect the selected agg implementation and auto-load any required train.csv-derived label statistics during initialization. Concrete agg modules MUST declare which of `npmi`, `label_idf`, and `label_frequency` they require, and `src/models/loss/mxclr.py` MUST consume that declaration without keeping a concrete-agg registry.

#### Scenario: Instantiate MXCLR with idf_chamfer without manual statistic injection

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr contrastive/model/agg@contrastive.model.loss_fn=idf_chamfer` を compose して model を instantiate する
- **THEN** MXCLR は `train.csv` から `npmi` と `label_idf` を自動ロードする
- **AND** `score_graph(labels)` は `ValueError("npmi is required for idf_chamfer.")` を送出しない

#### Scenario: Instantiate MXCLR transport agg without manual statistic injection

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr` の default agg または `wrd` `uot` を instantiate する
- **THEN** 各 agg が宣言した train.csv 由来統計が自動ロードされる
- **AND** `src/models/loss/mxclr.py` は concrete agg class の import や hard-coded family registry を持たない
