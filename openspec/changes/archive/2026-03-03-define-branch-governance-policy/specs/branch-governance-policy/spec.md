## ADDED Requirements

### Requirement: Topic branches must follow canonical naming format

Developers and coding agents MUST create implementation branches using `<type>/<topic>` naming.

#### Scenario: Accept canonical topic branch names

- **WHEN** 開発者または coding agent が実装用ブランチを作成する
- **THEN** ブランチ名は `<type>/<topic>` 形式である
- **AND** `type` は `feat` `fix` `refactor` `docs` `test` `chore` `exp` `ops` `hotfix` のいずれかである

### Requirement: Protected branches must not receive direct integration

Protected branches MUST be integrated via reviewable pull requests only.

#### Scenario: Reject direct push to protected branch

- **WHEN** `main` `dev` `release/*` への直接 push が試行される
- **THEN** 運用ゲートは push を拒否する
- **AND** 開発者は topic branch から PR を作成して統合する

### Requirement: Branch policy must be enforceable in local and remote controls

Project branch policy MUST be enforceable by local pre-push validation and SHOULD be mirrored with GitHub protected branch/ruleset controls.

#### Scenario: Local pre-push gate validates branch policy

- **WHEN** 開発者が push を実行する
- **THEN** pre-push hook は branch naming と protected branch 宛 push を検証する
- **AND** 違反時は非ゼロ終了で push を停止する

#### Scenario: Repository applies remote-side branch controls

- **WHEN** リポジトリ管理者がブランチ統制を設定する
- **THEN** protected branches/rulesets で PR 必須、status check 必須、直接更新制限を有効化する
