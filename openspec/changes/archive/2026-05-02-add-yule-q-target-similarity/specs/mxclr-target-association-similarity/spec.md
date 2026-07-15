## ADDED Requirements

### Requirement: MXCLR target association similarity must support corrected Yule's Q

MXCLR agg modules that blend label-description cosine similarity with NPMI MUST also support an explicit non-negative `yule_q_lambda` beta coefficient. The target label similarity MUST use the existing cosine/statistic blend weight as `alpha = 1.0 - transport_lambda` and combine terms as `alpha * cosine + (1.0 - alpha) * (npmi + yule_q_lambda * yule_q)`.

#### Scenario: Compute corrected Yule's Q from train labels

- **WHEN** label association statistics are computed from train.csv
- **THEN** pairwise Yule's Q uses Haldane-Anscombe 0.5 correction on all four contingency-table cells
- **AND** the returned matrix is finite, symmetric, diagonal-one, and mapped to the `[0, 1]` interval

#### Scenario: Blend cosine NPMI and Yule's Q in NPMI-aware aggs

- **WHEN** an NPMI-aware MXCLR agg receives label embeddings, NPMI, and Yule's Q with `yule_q_lambda > 0`
- **THEN** its label similarity matrix uses `alpha * cosine + (1.0 - alpha) * (npmi + yule_q_lambda * yule_q)` where `alpha = 1.0 - transport_lambda`
- **AND** the final label similarity matrix is clamped to the valid target range before graph aggregation or transport cost conversion

#### Scenario: Avoid unused Yule's Q computation when beta is zero

- **WHEN** an NPMI-aware MXCLR agg is configured with `yule_q_lambda = 0`
- **THEN** the agg does not request the Yule's Q label statistic
- **AND** the resulting target graph is equivalent to the existing cosine/NPMI blend for the same inputs
