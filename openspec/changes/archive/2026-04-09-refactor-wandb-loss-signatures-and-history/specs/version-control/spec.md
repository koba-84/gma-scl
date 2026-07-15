## ADDED Requirements

### Requirement: Topic branch history must be curated before push

Topic branch history prepared for review MUST remain linear and reviewable before push. Developers and coding agents MUST avoid merge-commit clutter in topic branches and MUST compact excessive commit chains before opening or updating a PR.

#### Scenario: Reject merge commits in topic-branch outgoing history

- **WHEN** 開発者または coding agent が topic branch を push する
- **THEN** upstream との差分レンジに merge commit が含まれないことを検証する
- **AND** merge commit が含まれる場合は push を失敗させ、rebase による線形化を促す

#### Scenario: Reject oversized outgoing commit chains

- **WHEN** 開発者または coding agent が topic branch を push する
- **THEN** upstream との差分 commit 数が上限値を超える場合は push を失敗させる
- **AND** interactive rebase / autosquash による履歴整理後に再 push する

### Requirement: History hygiene checks must be automatically enforceable

Repository tooling MUST provide an automated pre-push gate for history hygiene and allow explicit, auditable override knobs for exceptional cases.

#### Scenario: Enforce commit count cap with configurable threshold

- **WHEN** pre-push hook が実行される
- **THEN** commit 数上限は環境変数で明示的に調整可能である
- **AND** 未設定時は既定上限を適用して履歴肥大を防止する

#### Scenario: Allow explicit bypass for emergency operations

- **WHEN** 開発者または coding agent が緊急対応で履歴ゲートを一時回避する
- **THEN** 明示 bypass 環境変数を設定した場合のみ検証をスキップできる
- **AND** 標準運用では bypass を使用しない
