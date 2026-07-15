## MODIFIED Requirements

### Requirement: MXCLR rank loss must support agg-based MXCLR graph builders with a single lambda coefficient

The repository MUST provide `MXCLRKendall` as an MXCLR-family contrastive loss that reuses the same agg-based sample-graph builders as MXCLR, including the BERTScore variants. The ranking term MUST use differentiable Kendall τ, MUST be controlled by a single non-negative coefficient `lambda_rank`, and the implementation MUST NOT hide additional batch-size normalization inside that coefficient.

#### Scenario: Instantiate MXCLR Kendall config with reusable agg group

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr_kendall` を compose して instantiate する
- **THEN** `contrastive.model.loss_fn._target_` は `src.models.loss.mxclr_kendall.MXCLRKendall` として解決される
- **AND** `contrastive.model.loss_fn.agg` は `contrastive/model/agg@contrastive.model.loss_fn=<agg>` override で差し替えられる
- **AND** `BERTScore_F1` `BERTScore_Precision` `BERTScore_Recall` を含む既存 MXCLR agg config をそのまま使用できる

#### Scenario: Combine MXCLR and differentiable Kendall tau with explicit lambda rank

- **WHEN** 開発者または coding agent が `MXCLRKendall.forward(z, labels)` または `MXCLRKendall.forward(z, g_soft)` を実行する
- **THEN** 総損失は `MXCLR` の soft-target loss と differentiable Kendall τ ranking loss の和として計算される
- **AND** ranking 項の寄与は `lambda_rank * kendall_loss` で制御される
- **AND** Kendall τ の pairwise 比較は row-wise 標準化した teacher/student logits から計算される
- **AND** 実装は ranking 項を batch size で追加正規化しない
- **AND** self-pair の対角成分は ranking 項から除外される

#### Scenario: Control Kendall smoothness with explicit positive coefficient

- **WHEN** 開発者または coding agent が `contrastive.model.loss_fn.kendall_k` を設定して `MXCLRKendall` を初期化する
- **THEN** `kendall_k` は differentiable Kendall τ の tanh smoothness 係数として使用される
- **AND** `kendall_k` が 0 以下の場合は初期化時にエラーになる
