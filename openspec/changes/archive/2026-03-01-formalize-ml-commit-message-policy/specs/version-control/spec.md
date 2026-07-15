## ADDED Requirements

### Requirement: Commits must comply with commit message policy

開発者と coding agent は MUST commit 作成時に commit-message-policy 仕様へ準拠しなければならない。

#### Scenario: Create commit with policy-compliant message

- **WHEN** 開発者または coding agent が commit を作成する
- **THEN** commit message は commit-message-policy の件名・本文要件を満たす
- **AND** 逸脱する場合は理由を記録する
