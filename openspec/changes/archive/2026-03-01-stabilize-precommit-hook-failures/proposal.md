## Why

pre-commit の主要フックが環境依存・設定不整合で失敗し、コミット前品質ゲートが安定運用できていない。4つの失敗要因をタスクとして明示し、次セッションで順次解消できる状態にする。

## What Changes

- pre-commit 失敗中の 4 フック（interrogate, mdformat, bandit, shellcheck）を個別タスク化する。
- 各タスクに最小限の原因説明と完了条件を付与する。
- OpenSpec change 配下で管理し、引き継ぎ時の作業対象を明確化する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- dev-quality-tooling: pre-commit 失敗フックの安定化タスク要件を追加する。

## Impact

- 影響仕様: openspec/specs/dev-quality-tooling/spec.md
- 影響運用: 次セッションでの pre-commit 復旧作業を OpenSpec で追跡可能にする。
