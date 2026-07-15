### Requirement: MXCLR rank and Kendall losses must use distinct ranking objectives

The repository MUST provide `MXCLRRank` as the ListMLE rank variant and `MXCLRKendall` as the differentiable Kendall tau variant. Both losses MUST reuse MXCLR agg graph builders and MUST use `lambda_rank` as the ranking loss coefficient.

#### Scenario: MXCLRRank combines MXCLR with ListMLE

- **WHEN** 開発者または coding agent が `MXCLRRank.forward(z, labels)` または `MXCLRRank.forward(z, g_soft)` を実行する
- **THEN** 総損失は `MXCLR` の soft-target loss と row-wise ListMLE ranking loss の和として計算される
- **AND** ranking 項の寄与は `lambda_rank * listmle_loss` で制御される
- **AND** self-pair の対角成分は ListMLE ranking 項から除外される
- **AND** `MXCLRRank` は `kendall_k` を公開引数に持たない

#### Scenario: MXCLRKendall remains differentiable Kendall tau

- **WHEN** 開発者または coding agent が `MXCLRKendall.forward(z, labels)` または `MXCLRKendall.forward(z, g_soft)` を実行する
- **THEN** ranking 項は differentiable Kendall tau として計算される
- **AND** `kendall_k` は Kendall tau の tanh smoothness 係数として使用される
