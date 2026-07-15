## MODIFIED Requirements

### Requirement: Topic branch history must stay linear and reviewable before push

Topic branch pushes MUST keep outgoing history linear and composed of reviewable logical units. The repository MAY apply an additional commit-count cap, but only when that cap is explicitly configured as a local policy override.

#### Scenario: Block merge commits in outgoing topic-branch history

- **WHEN** 開発者または coding agent が topic branch を push する
- **THEN** outgoing history に merge commit が含まれていてはならない
- **AND** push 前に rebase で線形履歴へ整理する

#### Scenario: Optional commit-count cap is enforced only when configured

- **WHEN** `BRANCH_HISTORY_MAX_COMMITS` が明示設定されている
- **THEN** pre-push branch policy は outgoing commit 数がその値以下であることを検証する
- **AND** 未設定時は commit 数だけを理由に push を失敗させない

#### Scenario: Merge methods keep default-branch history streamlined

- **WHEN** topic branch を default branch へ統合する
- **THEN** squash merge または rebase merge のような streamlined/linear history を維持する merge method を優先する
- **AND** work-in-progress commit は default branch の履歴へそのまま残さない
