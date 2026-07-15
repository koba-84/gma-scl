## Context

現行仕様では commit ゲート未達時に commit を作成しないことは規定されているが、tasks チェック更新との前後関係が明文化されていない。結果として、実装は完了扱いでもコミット証跡が無い状態が発生し、引き継ぎ時の整合性が低下する。

## Goals / Non-Goals

**Goals:**

- タスク完了チェックとコミット証跡の整合ルールを明文化する。
- commit 不可時の扱いを「tasks 未完了 + blocked 報告」に統一する。
- dirty tree での実務対処を、許容手段と停止条件で明確化する。

**Non-Goals:**

- Git ワークフロー自体（branch 戦略や保護ルール）の変更。
- 自動マージや自動リリース運用の導入。

## Decisions

- Decision 1: tasks 完了チェックの前提として、同一論理変更の commit hash 記録を MUST とする。
  - Rationale: 完了判定の証跡を常に追跡可能にするため。
- Decision 2: commit ゲート未達時は tasks を完了化せず、blocked 理由と次アクションを必須報告する。
  - Rationale: 「完了」と「未コミット」の矛盾を排除するため。
- Decision 3: 混在差分時は、対象ファイル限定ステージングで分離できる場合のみ commit を許可し、不可なら停止してユーザー判断を待つ。
  - Rationale: 安全性を保ちながら、不要な作業停止を減らすため。

## Risks / Trade-offs

- [Risk] blocked 判定が増えて進行が遅く見える。
  - Mitigation: blocked 報告テンプレートに「不足条件」「必要なユーザー判断」「再開条件」を必須化する。
- [Risk] 対象ファイル限定コミットで取りこぼしが発生する。
  - Mitigation: commit 前に `git diff --cached --name-only` と OpenSpec tasks 対象ファイルを照合する。
