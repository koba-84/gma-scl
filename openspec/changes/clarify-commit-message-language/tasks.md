## 1. OpenSpec artifacts

- [x] 1.1 proposal/design/specs をレビューし、言語要件の境界（固定語と自由記述）を確定する

## 2. Implementation

- [x] 2.1 `openspec/specs/commit-message-policy/spec.md` に言語規約 requirement を同期する
- [x] 2.2 必要に応じて `scripts/validate_commit_message.py` の検証条件を更新する
- [x] 2.3 コミット運用ドキュメント（version-control 側）から参照可能な説明を追加する

## 3. Verification

- [x] 3.1 想定メッセージ（日本語本文・英語本文）で commit-msg 検証が意図通りになることを確認する
- [x] 3.2 `uv run pre-commit run -a` を実行して既存フックと競合しないことを確認する
