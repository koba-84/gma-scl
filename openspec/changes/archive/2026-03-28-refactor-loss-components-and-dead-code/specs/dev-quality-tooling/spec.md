## ADDED Requirements

### Requirement: Unused-code screening must use Vulture

The development workflow MUST provide a Vulture-based command to screen unused Python functions before human review and deletion.

#### Scenario: Run Vulture from repository configuration

- **WHEN** 開発者または coding agent が未使用関数候補を点検する
- **THEN** `uv run vulture` を `pyproject.toml` の repository-managed 設定で実行できる
- **AND** vulture は dev dependency として管理される
- **AND** 検出結果は削除確定ではなく review 候補として扱う
