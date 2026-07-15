## ADDED Requirements

### Requirement: Push destination must respect protected branch workflow

Developers and coding agents MUST avoid direct push integration to protected branches.

#### Scenario: Push from topic branch for review workflow

- **WHEN** 開発者または coding agent がリモートへ変更を送る
- **THEN** push 元は topic branch とし、統合は PR レビュー経由で実施する
- **AND** `main` `dev` `release/*` への直接 push を行わない
