## ADDED Requirements

### Requirement: MXCLR learned embedding similarity must support t-vMF kappa

MXCLR and MXCLRRank MUST expose a single non-negative `kappa` parameter for the
learned embedding-side sample-sample similarity transform. Implementations MUST
NOT expose a `similarity_type` switch for this behavior.

#### Scenario: Apply t-vMF transform after cosine similarity

- **WHEN** MXCLR or MXCLRRank computes learned embedding-side sample-sample
  cosine similarity `c`
- **THEN** it transforms the learned-side similarity as
  `(1.0 + c) / (1.0 + kappa * (1.0 - c)) - 1.0`
- **AND** `kappa=0` produces the same values as raw cosine similarity
- **AND** the reference-side graph `g_soft` and MXCLR agg modules are unchanged

#### Scenario: Resolve kappa from MXCLR family configs

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr` または
  `contrastive/model=mxclr_rank` を compose する
- **THEN** `contrastive.model.loss_fn.kappa` は config leaf として解決される
- **AND** `similarity_type` は解決対象に含まれない
