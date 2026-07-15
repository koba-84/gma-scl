## ADDED Requirements

### Requirement: MXCLR aggregation mode selection

MXCLR MUST accept an initialization argument agg and switch label-set aggregation behavior in similarity_graph according to that value.

#### Scenario: Initialize MXCLR with supported agg value

- **WHEN** 開発者が `MXCLR(..., agg="mean")` または `MXCLR(..., agg="self_norm")` で初期化する
- **THEN** 初期化は成功し、指定した agg が以後の similarity_graph 計算に適用される

#### Scenario: Initialize MXCLR with unsupported agg value

- **WHEN** 開発者が未対応値（例: `agg="foo"`）で MXCLR を初期化する
- **THEN** MXCLR は学習開始前に ValueError を送出する

### Requirement: MXCLR must reuse shared aggregation contract

MXCLR.similarity_graph MUST follow the shared aggregation contract defined in openspec/specs/training/spec.md and MUST NOT redefine branch formulas locally in a conflicting way.

#### Scenario: Resolve MXCLR aggregation formulas from shared contract

- **WHEN** 開発者が MXCLR の agg 分岐仕様を確認する
- **THEN** `mean/self_norm` の式は openspec/specs/training/spec.md の共通集約契約を参照して解釈する
- **AND** MXCLR 固有仕様は `similarity_graph(labels)` で追加変換を入れない点のみを規定する
