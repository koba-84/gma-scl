## ADDED Requirements

### Requirement: Completed changes must be archived autonomously without extra prompt

Developers and coding agents MUST archive a completed OpenSpec change immediately after completion checks pass, without waiting for additional user instruction.

#### Scenario: Auto-archive right after completion checks

- **WHEN** `openspec status --change <name>` が complete であり、`tasks.md` に未完了チェックがない
- **THEN** coding agent は追加指示なしで archive 実行に進む
- **AND** archive 先は `openspec/changes/archive/YYYY-MM-DD-<change-name>` 命名規約を使用する

#### Scenario: Stop and report when archive preconditions fail

- **WHEN** archive 先の同名パス存在、対象外差分混在、または移行後検証失敗により archive を安全に完了できない
- **THEN** coding agent は archive を実行せず停止する
- **AND** 停止理由と解消に必要な次アクションを報告する
