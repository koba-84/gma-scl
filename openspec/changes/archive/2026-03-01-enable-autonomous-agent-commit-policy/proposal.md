## Why

commit タイミング自体は規定済みだが、coding agent がユーザー追加指示なしで commit を実行してよい条件が仕様化されていない。自律実行の境界を明確にし、再現性と安全性を維持したまま運用できる状態にする。

## What Changes

- coding agent の自律 commit 実行条件（必須前提、禁止条件、停止条件）を仕様化する。
- 自律 commit 前に必要な品質ゲート（pre-commit 成功、Python 変更時の型チェック通過）を明示する。
- branch 保護とレビュー前提の運用に合わせ、agent が merge や保護ブランチ直接 push を行わない規約を追加する。
- 上記ルールの根拠として git 公式・GitHub Docs・GitHub Copilot Docs の一次情報を仕様に残す。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- agent-operation-policy: coding agent が自律 commit 可能な条件と停止条件を追加する。
- dev-quality-tooling: 自律 commit 前提の品質ゲート要件を明確化する。

## Impact

- 影響仕様: openspec/specs/agent-operation-policy/spec.md, openspec/specs/dev-quality-tooling/spec.md, openspec/specs/version-control.md
- 影響運用: coding agent の commit 実行判断が仕様準拠で自動化可能になる。
