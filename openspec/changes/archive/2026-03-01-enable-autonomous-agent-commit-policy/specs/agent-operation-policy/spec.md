## ADDED Requirements

### Requirement: Agent autonomous commit execution gate

Coding agent MUST execute commit autonomously when all commit gate conditions are satisfied, and MUST NOT commit when any gate fails.

#### Scenario: Execute autonomous commit on satisfied gate

- **WHEN** 単一 OpenSpec change の対象実装が完了し、必須検証が成功し、commit 単位が単一論理変更に分離されている
- **THEN** coding agent は追加のユーザー明示指示なしで commit を作成する
- **AND** report には commit hash と実行検証コマンドを含める

#### Scenario: Block autonomous commit on gate failure

- **WHEN** 必須検証が未実行または失敗、もしくは対象外差分の混在が解消できない
- **THEN** coding agent は commit を作成してはならない
- **AND** 失敗条件を報告し、停止する

### Requirement: Agent must avoid protected-branch direct integration

Coding agent MUST NOT bypass review controls by directly integrating to protected branches.

#### Scenario: Respect protected-branch workflow

- **WHEN** リモート統合が protected branch の対象である
- **THEN** coding agent は protected branch への直接 push や merge を行ってはならない
- **AND** review 可能な commit 境界または PR 提出情報を報告する
