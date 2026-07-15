## Context

現行の commit-message-policy は件名構造と本文セクションを規定しているが、本文言語の明示ルールがない。研究運用では日本語の説明が必要な場面と、機械検証向けの英語キーワードを固定したい場面が混在している。

## Goals / Non-Goals

**Goals:**

- 必須構造の固定語（Type, Why, Validation, Reproducibility）を明確化する。
- 本文説明は日本語/英語のいずれでも許容する運用を明文化する。
- 将来のフック実装が判定可能な粒度で requirement を記述する。

**Non-Goals:**

- 既存コミット履歴の書き換え。
- 全文自然言語の厳密自動判定。
- 文体ガイド（敬体/常体など）の統一。

## Decisions

1. 言語ルールは `commit-message-policy` capability の ADDED Requirement として追加する。
   理由: 既存 requirement を壊さずに運用契約を拡張できる。

2. 件名の Type と本文の必須セクション名は英語固定とする。
   理由: 既存フックと互換的で、機械検証が容易。

3. セクション本文は日本語または英語を許容する。
   理由: チーム内の可読性と実務運用を両立する。

## Risks / Trade-offs

- [Risk] 自然言語判定を厳密化すると誤検知が増える。
  Mitigation: まずは固定キーワードのみを必須化し、本文言語自体は許容制にする。
- [Risk] 既存フックが未対応だと仕様と実装が一時不整合になる。
  Mitigation: tasks でフック更新タスクを明示し、実装 change で追従する。
