## 1. OpenSpec Artifacts

- [x] 1.1 proposal.md に commit タイミング明確化の目的と影響範囲を定義する
- [x] 1.2 design.md に dirty tree 対応と commit 実行条件を定義する
- [x] 1.3 specs/version-control・specs/dev-quality-tooling・specs/agent-operation-policy の要件を作成する

## 2. Main Spec Update

- [x] 2.1 openspec/specs/version-control.md に commit タイミング要件と dirty tree 開始時ルールを追加する
- [x] 2.2 openspec/specs/dev-quality-tooling/spec.md に commit 直前ゲート要件を追加する
- [x] 2.3 openspec/specs/agent-operation-policy/spec.md を新規追加する

## 3. Verification

- [x] 3.1 `uv run openspec validate formalize-agent-commit-timing-policy --type change --strict` が成功することを確認する
- [x] 3.2 `uv run openspec status --change formalize-agent-commit-timing-policy` で完了状態を確認する
