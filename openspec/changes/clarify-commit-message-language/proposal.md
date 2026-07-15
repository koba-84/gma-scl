## Why

コミットメッセージの書式は定義されているが、本文言語の扱いが曖昧で、レビュー時に表記揺れが発生している。言語運用の契約を明示し、履歴の可読性と自動検証の安定性を上げる。

## What Changes

- commit message の言語運用を仕様化する。
- 件名フォーマットの言語固定要素（Type と主要ヘッダ）を明確化する。
- 本文の許容言語範囲（日本語/英語）と必須セクション表記を定義する。

## Capabilities

### New Capabilities
- なし

### Modified Capabilities
- `commit-message-policy`: コミットメッセージ言語の必須表記ルールを追加する

## Impact

- 影響仕様: `openspec/specs/commit-message-policy/spec.md`
- 影響運用: commit 作成時の本文記述規約
- 実装影響候補: `scripts/validate_commit_msg.py`（必要に応じて検証強化）
