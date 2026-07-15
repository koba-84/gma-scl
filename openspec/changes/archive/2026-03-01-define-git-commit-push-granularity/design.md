## Context

既存仕様には学習・評価の実行規約はあるが、変更履歴管理の規約が不足しています。そのため、1回の commit に複数トピックが混ざる、push の時点で未検証変更が混在する、といった運用揺れが発生しやすい状態です。

Context7 で確認した git 公式ドキュメント（user-manual.adoc）でも、各 patch は単一の論理変更を持つことが推奨されています。ローカル履歴でも、主語が明確な単位（例: Refactor..., Add..., Migrate...）は追跡しやすく、複数論点が混在した履歴より再現調査が容易でした。

## Goals / Non-Goals

Goals:

- commit を論理変更単位で固定する。
- push をレビュー可能な変更セット単位で固定する。
- commit/push 前の最小検証を明文化する。

Non-Goals:

- GitHub Flow や trunk-based などブランチ戦略そのものの強制。
- 過去履歴の書き換え運用（rebase -i）の必須化。

## Decisions

- main spec として `openspec/specs/version-control.md` を追加し、Git 変更管理規約を定義する。
- commit 粒度は MUST で以下を要求する。
  - 1 commit は単一の論理変更のみを含む。
  - その commit だけを適用しても設定解決または該当テストが成立する。
  - 無関係な整形・リネーム・機能変更を同一 commit に混在させない。
- push 粒度は MUST で以下を要求する。
  - 1 push は同一トピック change の commit 群に限定する。
  - push 前に fast テスト（-m "not slow"）を通す。
  - 失敗中の暫定 commit は squash/fixup 済みである。
- commit メッセージは SHOULD で以下を推奨する。
  - 先頭を動詞（Add/Fix/Refactor/Docs/Test/Chore）で開始する。
  - 何を変えたかを 60 文字前後で示す。
  - 必要なら本文に実行コマンドと結果を追記する。

## Risks / Trade-offs

- Risk: commit 数が増える。
  - Mitigation: push 前に topic 単位で整理し、レビュー負荷を制御する。
- Risk: fast テスト実行の時間コスト。
  - Mitigation: slow は分離し、push 前は fast に限定する。
