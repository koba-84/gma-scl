## ADDED Requirements

### Requirement: Commit message policy must be enforced automatically

Project MUST enforce commit message policy through executable gates at commit time and push time.

#### Scenario: Validate message on commit

- **WHEN** 開発者または coding agent が commit を作成する
- **THEN** commit-msg フックで件名形式と必須本文項目を検証する
- **AND** 不一致時は commit を失敗させる

#### Scenario: Validate outgoing commits on push

- **WHEN** 開発者または coding agent が push を実行する
- **THEN** pre-push フックで push 対象コミット群の message 要件を再検証する
- **AND** 不一致時は push を失敗させる
