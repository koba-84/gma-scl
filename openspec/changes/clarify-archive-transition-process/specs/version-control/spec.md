## ADDED Requirements

### Requirement: OpenSpec change archive transition process

Developers and coding agents MUST move completed OpenSpec changes from active changes to archive using a minimal deterministic process.

#### Scenario: Allow archive only for completed change

- **WHEN** 開発者または coding agent が `openspec/changes/<name>` を archive へ移行する
- **THEN** `openspec status --change <name>` が complete であることを確認する
- **AND** tasks チェックボックスに未完了がないことを確認する

#### Scenario: Move change with canonical archive path and no overwrite

- **WHEN** archive 実行を行う
- **THEN** 移行先は `openspec/changes/archive/YYYY-MM-DD-<change-name>` 命名規約を使用する
- **AND** 同名パスが既存の場合は上書きせずに処理を停止する

#### Scenario: Verify post-archive state

- **WHEN** archive 移行が完了した
- **THEN** 元の `openspec/changes/<name>` に change ディレクトリが存在しないことを確認する
- **AND** archive 側に `openspec/changes/archive/YYYY-MM-DD-<change-name>` が存在することを確認する
