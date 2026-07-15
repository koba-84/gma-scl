## MODIFIED Requirements

### Requirement: MXCLR rank loss must support agg-based MXCLR graph builders with a single lambda coefficient

The repository MUST provide `MXCLRRank` as an MXCLR-family contrastive loss that reuses the same agg-based sample-graph builders as MXCLR, including the BERTScore variants. The ranking term MUST be controlled by a single non-negative coefficient `lambda_rank`, and the implementation MUST NOT hide additional batch-size normalization inside that coefficient.

#### Scenario: Instantiate MXCLR rank config with reusable agg group

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr_rank` を compose して instantiate する
- **THEN** `contrastive.model.loss_fn._target_` は `src.models.loss.mxclr_rank.MXCLRRank` として解決される
- **AND** `contrastive.model.loss_fn.agg` は `contrastive/model/agg@contrastive.model.loss_fn=<agg>` override で差し替えられる
- **AND** `BERTScore_F1` `BERTScore_Precision` `BERTScore_Recall` を含む既存 MXCLR agg config をそのまま使用できる

#### Scenario: Combine MXCLR and ListMLE with explicit lambda rank

- **WHEN** 開発者または coding agent が `MXCLRRank.forward(z, labels)` または `MXCLRRank.forward(z, g_soft)` を実行する
- **THEN** 総損失は `MXCLR` の soft-target loss と row-wise `ListMLE` loss の和として計算される
- **AND** ranking 項の寄与は `lambda_rank * listmle_loss` で制御される
- **AND** 実装は ranking 項を batch size で追加正規化しない
- **AND** self-pair の対角成分は ranking 項から除外される
