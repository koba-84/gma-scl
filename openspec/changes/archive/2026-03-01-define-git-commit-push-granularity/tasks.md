## 1. OpenSpec Artifacts

- [x] 1.1 proposal.md に commit/push 粒度標準化の目的と影響範囲を定義する
- [x] 1.2 design.md に commit/push 粒度と検証ゲートの方針を定義する
- [x] 1.3 specs/version-control/spec.md に要件とシナリオを追加する

## 2. Main Spec Update

- [x] 2.1 openspec/specs/version-control.md に commit 粒度規約を追加する
- [x] 2.2 openspec/specs/version-control.md に push 粒度規約を追加する
- [x] 2.3 openspec/specs/version-control.md に commit/push 前の最小検証手順を追加する

## 3. Verification

- [x] 3.1 uv run openspec validate define-git-commit-push-granularity --type change --strict が成功することを確認する
- [x] 3.2 uv run openspec status --change define-git-commit-push-granularity で完了状態を確認する
