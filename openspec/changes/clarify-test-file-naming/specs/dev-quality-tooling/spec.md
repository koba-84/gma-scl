## MODIFIED Requirements

### Requirement: Pytest test file naming consistency

Test files under `tests/` SHALL use topic-based names without a `test_` prefix, and the naming convention SHALL remain aligned with the configured pytest collection pattern.

#### Scenario: Add a new test file under tests directory

- **WHEN** 開発者または coding agent が `tests/` 配下に新規テストファイルを追加する
- **THEN** ファイル名は `<topic>.py` 形式を使用し `test_` 接頭辞を付けない
- **AND** 命名は `pyproject.toml` の pytest 収集設定と矛盾しない
