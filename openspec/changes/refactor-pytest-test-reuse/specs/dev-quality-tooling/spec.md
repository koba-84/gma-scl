## MODIFIED Requirements

### Requirement: Pytest shared setup reuse

Pytest test modules that need the same setup across multiple tests MUST centralize that setup in shared fixtures instead of duplicating arrange and cleanup logic per test.

#### Scenario: Reuse synthetic datasets and common initialization

- **WHEN** 開発者または coding agent が複数テストで同じ temporary dataset、Hydra 初期化、monkeypatch 群を必要とする pytest module を実装または更新する
- **THEN** 共有 setup は `tests/conftest.py` または pytest fixture から再利用可能な helper に集約される
- **AND** 個別テストはケース固有の入力差分と assertion のみを持つ
- **AND** `try/finally` による手動 cleanup や重複した初期化コードを各テストへ繰り返さない

### Requirement: Parametrized case visibility

Pytest test modules with repeated assertions over independent case data MUST express those cases through parametrization so failures remain independently visible.

#### Scenario: Report each supported case independently

- **WHEN** 開発者または coding agent が同一 test body で loss variant、command variant、success/failure branch など独立したケースを検証する
- **THEN** `@pytest.mark.parametrize` または同等の pytest 機構でケースを列挙する
- **AND** 各ケースは pytest の収集結果と失敗出力で独立した test case として識別できる
- **AND** 必要に応じて `ids` または `pytest.param(..., id=...)` でケース名を安定化する
