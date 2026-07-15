### Requirement: MXCLR rank and Kendall losses must both be selectable

The repository MUST provide both `mxclr_rank` and `mxclr_kendall` as explicit MXCLR-family contrastive loss configs. Both losses MUST reuse MXCLR agg graph builders and MUST combine MXCLR soft-target loss with differentiable Kendall tau controlled by `lambda_rank`.

#### Scenario: Instantiate MXCLR rank config

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr_rank` を compose して instantiate する
- **THEN** `contrastive.model.loss_fn._target_` は `src.models.loss.mxclr_rank.MXCLRRank` として解決される
- **AND** `contrastive.model.loss_fn.agg` は `contrastive/model/agg@contrastive.model.loss_fn=<agg>` override で差し替えられる
- **AND** `MXCLRRank.forward(z, labels)` と `MXCLRRank.forward(z, g_soft)` は MXCLR soft-target loss と differentiable Kendall tau ranking loss の和を返す

#### Scenario: Keep MXCLR Kendall config selectable

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr_kendall` を compose して instantiate する
- **THEN** `contrastive.model.loss_fn._target_` は `src.models.loss.mxclr_kendall.MXCLRKendall` として解決される
- **AND** `lambda_rank` と `kendall_k` は明示 config key として解決される

### Requirement: MXCLR-family losses must not apply agg regularizers

MXCLR-family contrastive losses MUST NOT call agg-level regularizer hooks. Supported agg implementations MUST only build sample score graphs from labels and label statistics.

#### Scenario: Labels path has no extra regularizer term

- **WHEN** MXCLR-family loss が `forward(z, labels)` を実行する
- **THEN** 損失は score graph 由来の contrastive objective だけで計算される
- **AND** agg object の `regularizer` attribute は公開契約に含まれない

### Requirement: Unsupported MXCLR agg choices must be removed

The repository MUST NOT expose `self_norm`, `distill_chamfer`, or `distill_idf_chamfer` as supported contrastive model agg choices.

#### Scenario: Supported agg config set excludes removed choices

- **WHEN** 開発者または coding agent が `configs/contrastive/model/agg/*.yaml` を確認する
- **THEN** `self_norm.yaml`, `distill_chamfer.yaml`, and `distill_idf_chamfer.yaml` は存在しない
- **AND** supported MXCLR-family agg choices are limited to maintained graph builders such as `mean`, `chamfer`, `idf_chamfer`, `uot`, `wmd`, `wrd`, and BERTScore variants
