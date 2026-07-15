## ADDED Requirements

### Requirement: MCACR aggregation mode selection

MCACRLoss MUST accept an initialization argument agg and switch repulsion-side similarity aggregation according to that value.

#### Scenario: Initialize MCACR with supported agg value

- **WHEN** 開発者が `MCACRLoss(..., agg="mean")` または `MCACRLoss(..., agg="self_norm")` で初期化する
- **THEN** 初期化は成功し、指定 agg が repulsion 重み計算に適用される

#### Scenario: Initialize MCACR with unsupported agg value

- **WHEN** 開発者が未対応値（例: `agg="foo"`）で MCACR を初期化する
- **THEN** MCACR は学習開始前に ValueError を送出する

### Requirement: MCACR must reuse shared aggregation contract

MCACRLoss repulsion similarity MUST follow the shared aggregation contract defined in openspec/specs/training/spec.md and MUST apply repulsion weighting after that aggregation.

#### Scenario: Resolve MCACR aggregation formulas from shared contract

- **WHEN** 開発者が MCACR の agg 分岐仕様を確認する
- **THEN** `mean/self_norm` の式は openspec/specs/training/spec.md の共通集約契約を参照して解釈する
- **AND** MCACR 固有仕様は後段で `repulse_weight = (1-sim)^beta` を適用する点を規定する
