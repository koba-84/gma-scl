## Context

現状の pre-commit は、docstring カバレッジ不足、Markdown 整形依存不整合、bandit 実行依存欠落、shellcheck 警告の4系統で失敗している。修正対象が異なるため、次セッションで個別に切り分けて解消する必要がある。

## Goals / Non-Goals

**Goals:**

- 4つの失敗要因を独立タスクとして定義する。
- 各タスクで「何を直せば通るか」を一文で明確化する。

**Non-Goals:**

- 本 change 内で実際のフック修正を完了すること。
- pre-commit 以外の品質ゲート追加。

## Decisions

- Decision 1: 4フックを1タスク1原因で分離する。
  - Rationale: 次セッションで並列または段階的に処理しやすい。
- Decision 2: タスク文に原因と完了条件を含める。
  - Rationale: 引き継ぎ時に追加調査コストを減らせる。

## Risks / Trade-offs

- [Risk] 実際の修正順で副作用が出る可能性がある。→ Mitigation: 各タスク完了後に `uv run pre-commit run -a` を再実行して差分確認する。
