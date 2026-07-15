### Requirement: MXCLRRank ListMLE must use a dedicated rank temperature

`MXCLRRank` MUST expose a positive `rank_temperature` argument for the ListMLE ranking term. The ListMLE student scores MUST use `rank_temperature`, while the MXCLR soft-target objective MUST continue to use `instance_temperature`.

#### Scenario: Instantiate MXCLRRank with explicit rank temperature

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr_rank` を compose して instantiate する
- **THEN** `contrastive.model.loss_fn.rank_temperature` は config に明示される
- **AND** `rank_temperature` は `MXCLRRank.__init__` の runtime 引数として解決される

#### Scenario: Compute ListMLE with rank temperature

- **WHEN** `MXCLRRank.forward(z, labels)` または `MXCLRRank.forward(z, g_soft)` を実行する
- **THEN** MXCLR soft-target loss は `instance_temperature` を使う
- **AND** ListMLE ranking 項の student scores は `rank_temperature` で scaling される
- **AND** `rank_temperature` が 0 以下の場合は初期化時にエラーになる
