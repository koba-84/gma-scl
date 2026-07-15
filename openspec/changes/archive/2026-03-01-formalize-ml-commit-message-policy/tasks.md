## 1. OpenSpec Artifacts

- [x] 1.1 proposal.md に commit message 規約強化の目的と影響範囲を定義する
- [x] 1.2 design.md に件名・本文・ML再現情報の設計方針を定義する
- [x] 1.3 specs/version-control と specs/commit-message-policy の要件を作成する

## 2. Main Spec Update

- [x] 2.1 openspec/specs/version-control.md に commit-message-policy 準拠要件を追加する
- [x] 2.2 openspec/specs/commit-message-policy/spec.md を新規作成する

## 3. Verification

- [x] 3.1 `uv run openspec validate formalize-ml-commit-message-policy --type change --strict` が成功することを確認する
- [x] 3.2 `uv run openspec status --change formalize-ml-commit-message-policy` で完了状態を確認する
