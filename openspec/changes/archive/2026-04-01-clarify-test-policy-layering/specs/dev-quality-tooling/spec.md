## ADDED Requirements

### Requirement: Pytest test layering policy must define where each contract is checked

Pytest and self-test organization MUST separate shared integration contracts, property-level invariants, and component-specific compatibility regressions so maintainers can tell where a failure belongs.

#### Scenario: Map a new test to the correct layer

- **WHEN** 開発者または coding agent が test を追加または整理する
- **THEN** pure function や algebraic invariant は property-based test または component self-test に配置する
- **AND** multi-component wiring や Hydra/DataModule/stage integration は pytest integration test に配置する
- **AND** 特定実装だけが持つ third-party compatibility や runtime hygiene は component-specific regression test として個別に保持できる

## MODIFIED Requirements

### Requirement: Parametrized case visibility

Pytest test modules with repeated assertions over independent case data MUST express those cases through parametrization so failures remain independently visible. Parametrization MUST be used only when the repeated cases exercise the same behavioral contract; distinct contracts MUST remain separate tests even if they share the same subsystem name.

#### Scenario: Report each supported case independently

- **WHEN** 開発者または coding agent が同一 test body で loss variant、command variant、success/failure branch など独立したケースを検証する
- **THEN** `@pytest.mark.parametrize` または同等の pytest 機構でケースを列挙する
- **AND** 各ケースは pytest の収集結果と失敗出力で独立した test case として識別できる
- **AND** 必要に応じて `ids` または `pytest.param(..., id=...)` でケース名を安定化する

#### Scenario: Keep distinct contracts as separate tests

- **WHEN** 開発者または coding agent が同一 subsystem に属するが assertion の意味が異なる test を整理する
- **THEN** 共通 setup は fixture に集約してよい
- **AND** third-party stdout 抑止、初期化順序エラー、数理的不変条件のような別契約は 1 本の parametrized test に無理に統合しない
- **AND** test 名や file 名は検証している contract を直接示す
