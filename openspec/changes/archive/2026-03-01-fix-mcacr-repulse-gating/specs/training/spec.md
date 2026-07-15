## MODIFIED Requirements

### Requirement: MCACR repulsion gating by positive availability

This requirement SHALL gate the MCACR-family repulsion term by positive availability, and MUST zero repulsion only when an anchor has no positives.

#### Scenario: positive が存在し attraction 距離が 0 の場合

- WHEN MCACR または MCACR_WONEG の forward が、正例を含むアンカーで attraction 項が 0 となる入力を受ける
- THEN そのアンカーの repulsion 項は 0 化されない

#### Scenario: positive が存在しない場合

- WHEN MCACR または MCACR_WONEG の forward が、正例を持たないアンカーを含む入力を受ける
- THEN そのアンカーの repulsion 項は 0 化される
