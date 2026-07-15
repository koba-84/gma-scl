## MODIFIED Requirements

### Requirement: Pytest shared setup reuse

Pytest test modules that need the same setup across multiple tests MUST centralize that setup in shared fixtures instead of duplicating arrange and cleanup logic per test. Domain-specific shared fixtures SHOULD live in dedicated modules under `tests/support/fixtures/`, while the root `tests/conftest.py` SHOULD stay limited to global pytest configuration and fixture-module registration.

#### Scenario: Reuse synthetic datasets and common initialization

- **WHEN** 開発者または coding agent が複数テストで同じ temporary dataset、Hydra 初期化、monkeypatch 群を必要とする pytest module を実装または更新する
- **THEN** 共有 setup は `tests/conftest.py` または `tests/support/fixtures/` 配下の pytest fixture module から再利用可能に集約される
- **AND** 個別テストはケース固有の入力差分と assertion のみを持つ
- **AND** `try/finally` による手動 cleanup や重複した初期化コードを各テストへ繰り返さない

### Requirement: Pytest test layering policy must define where each contract is checked

Pytest and self-test organization MUST separate shared integration contracts, property-level invariants, and component-specific compatibility regressions so maintainers can tell where a failure belongs. The directory layout SHOULD reflect that separation by keeping component regression tests under domain directories such as `tests/losses/`, property-based invariants under `tests/property/`, and multi-component train/data contracts under `tests/integration/`.

#### Scenario: Map a new test to the correct layer

- **WHEN** 開発者または coding agent が test を追加または整理する
- **THEN** pure function や algebraic invariant は `tests/property/` 配下の property-based test に配置する
- **AND** multi-component wiring や Hydra/DataModule/stage integration は `tests/integration/` 配下に配置する
- **AND** 特定実装だけが持つ third-party compatibility や runtime hygiene は `tests/losses/` など対象 domain の regression test として個別に保持できる
