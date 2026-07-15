## Why

作業報告で commit 粒度や実行検証の記載漏れが発生すると、レビュー側の確認コストが増える。報告前に機械的に確認できる自己点検フローを追加して、漏れを事前に防ぐ必要がある。

## What Changes

- 報告前点検スクリプトを追加し、OpenSpec 完了状態・コミット履歴・検証コマンド結果をまとめて確認可能にする。
- 報告テンプレートの必須項目を文書化する。
- training spec に報告前自己点検の実行要件を追記する。

## Capabilities

### New Capabilities

- `delivery-self-check`: 報告前自己点検の標準手順。

### Modified Capabilities

- `training`: commit/push 運用に報告前自己点検を追加。

## Impact

- 影響ファイル: `scripts/verify_delivery.sh`, `docs/delivery_self_check.md`, `openspec/specs/training/spec.md`
