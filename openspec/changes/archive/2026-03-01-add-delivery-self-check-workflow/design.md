## Context

現状は報告内容の網羅性を人手確認に依存している。とくに commit 粒度と OpenSpec change 完了状態、実行検証コマンドの記載漏れが起きやすい。

## Goals / Non-Goals

**Goals:**

- 1コマンドで報告前チェックを実行し、失敗時に非0終了する。
- 報告テンプレートを固定し、最低限の記載項目を標準化する。

**Non-Goals:**

- CI/CD の導入。
- 既存テスト群の置き換え。

## Decisions

- `scripts/verify_delivery.sh` を追加し、以下を検証する。
  - 指定 OpenSpec change の `isComplete=true`
  - 指定検証コマンドの成功
  - 直近コミット一覧の出力
- `docs/delivery_self_check.md` で運用手順と報告テンプレートを定義する。

## Risks / Trade-offs

- [Risk] スクリプト未実行で従来どおり漏れが起きる。 → Mitigation: spec に MUST 要件として追記し、運用で必須化する。
- [Risk] チェック項目が不足する。 → Mitigation: `--run` オプションで案件別コマンドを追加可能にする。
