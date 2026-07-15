## Context

現在の運用では、change が完了しても archive 実行タイミングが担当者判断に委ねられています。そのため、完了済み change が active 側に残留し、状態把握と運用再現性が低下します。

## Goals / Non-Goals

**Goals:**
- tasks 完了後に archive 前提条件を満たす場合、coding agent が自律的に archive を実行する要件を追加する。
- 自律実行できない場合の停止理由と次アクション報告を要件化する。

**Non-Goals:**
- archive コマンド実装の新規追加。
- OpenSpec CLI の仕様変更。

## Decisions

- archive タイミング要件は `version-control` に追加し、完了後の実行を MUST 化する。
- agent の行動要件は `agent-operation-policy` に追加し、実行不能時の停止報告を MUST 化する。
- 既存の archive 安全要件（complete 判定、未完了 task なし、同名衝突チェック）は維持する。

## Risks / Trade-offs

- [Risk] 自律 archive により確認なしで移行される懸念 → Mitigation: 前提条件と確認コマンドを仕様で固定し、失敗時は停止報告を義務化。
- [Risk] 対象外 dirty 差分で archive 実行が失敗 → Mitigation: 混在時は実行せず理由を即時報告する要件を追加。
