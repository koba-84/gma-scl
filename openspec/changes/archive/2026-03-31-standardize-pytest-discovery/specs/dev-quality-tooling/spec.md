## MODIFIED Requirements

### Requirement: Pytest test file naming consistency

Test files under `tests/` SHALL use pytest standard discovery naming, and support code used by tests SHALL NOT rely on the same file discovery rule as collected test modules.

#### Scenario: Add a new collected test module under tests directory

- **WHEN** 開発者または coding agent が `tests/` 配下に新規 test module を追加する
- **THEN** ファイル名は `test_<topic>.py` または `<topic>_test.py` 形式を使用する
- **AND** 命名は pytest 標準 discovery と矛盾しない

#### Scenario: Add support code for tests

- **WHEN** 開発者または coding agent が test 支援用の Python module を追加する
- **THEN** その module は collected test modules とは別の support 領域へ配置される
- **AND** support code は `python_files` の拡張設定に依存せず import される
