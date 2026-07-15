## ADDED Requirements

### Requirement: Shared aggregation contract for contrastive losses

The specification MUST define one shared contract for agg-based label aggregation and reuse it across losses instead of duplicating formulas.

#### Scenario: Define shared agg contract once

- **WHEN** 開発者が training main spec を参照する
- **THEN** `agg` の許可値、`mean/self_norm` の式、数値制約は単一箇所で定義される

#### Scenario: Loss-specific sections reference shared contract

- **WHEN** 開発者が MCACR または MXCLR の節を参照する
- **THEN** 各節は共通契約を参照し、loss 固有の責務のみを追記する

## MODIFIED Requirements

### Requirement: Contrastive loss naming and contract consistency

The specification SHALL define consistent names and contracts for contrastive losses in one coherent section.

#### Scenario: Keep contracts consistent across losses

- **WHEN** agg 分岐式の変更が発生する
- **THEN** 変更は共通契約の単一箇所を更新すれば反映できる
- **AND** MCACR/MXCLR 節の式重複更新を要求しない
