## MODIFIED Requirements

### Requirement: Pytest shared setup reuse

Pytest test modules that need the same setup across multiple tests MUST centralize that setup in shared fixtures instead of duplicating arrange and cleanup logic per test.

#### Scenario: Reuse runtime stubs and MXCLR test assets

- **WHEN** 開発者または coding agent が logging runtime stub、temporary dataset、`label_descriptions.json`、MXCLR encoder monkeypatch のような同一 setup を複数 test module で使う
- **THEN** setup は `tests/conftest.py` などの shared fixture に集約される
- **AND** test module 内では必要最小限のケース差分だけを記述する
- **AND** `tmp_path` で代替可能な一時領域管理に `uuid` と手動 `shutil.rmtree` を使わない
