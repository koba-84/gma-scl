## Context

Git 公式の patch/workflow ガイドは単一論理変更と説明可能な履歴を推奨している。Conventional Commits は件名フォーマットの共通化を提供し、GitHub Docs は小さく焦点化した PR を推奨している。ML 文脈では、実験再現に commit hash と設定差分の追跡が必要であり、メッセージ本文に「なぜ」「何を」「どう検証したか」を残す価値が高い。

現状仕様には commit 粒度と timing はあるが、本文に最低限残す内容が曖昧なため、同種変更でも説明密度が揺れる。

## Goals / Non-Goals

**Goals:**

- commit 件名の統一フォーマットを定義する。
- commit 本文の必須/推奨フィールドを定義する。
- ML 変更時の再現情報（設定・検証）の記録ルールを定義する。
- OpenSpec change と commit の紐付け運用を明確化する。

**Non-Goals:**

- Conventional Commits の厳密強制（完全準拠 parser の導入）。
- 既存履歴の書き換え。
- すべての commit で長文本文を必須化すること。

## Decisions

- 新規 spec `commit-message-policy` を追加し、件名・本文・ML補足の 3 層要件を定義する。
- 件名は `<type>: <summary>` を推奨し、type は既存運用語彙（Feat/Fix/Refactor/Docs/Test/Chore）を標準にする。
- 本文は「Why」「What」「Validation」の3要素を推奨し、挙動変更を含む場合は Validation を MUST にする。
- ML 変更（model/loss/sampler/data/hparams）では、本文に少なくとも対象設定キーまたは設定ファイルを明記することを MUST にする。
- 既存 `version-control` には「commit は commit-message-policy に従う」を追加して仕様間整合を確保する。

## Risks / Trade-offs

- [Risk] 記述負荷が増える -> Mitigation: docs/test/chore の軽量変更は1行本文を許容する。
- [Risk] 過剰に形式化すると速度低下 -> Mitigation: MUST は最小限（再現性に直結する項目）に限定する。
- [Risk] 既存メッセージ慣習との差異 -> Mitigation: 既存 type 語彙を維持し、移行コストを下げる。
