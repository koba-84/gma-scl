## 1. OpenSpec artifacts

- [x] 1.1 proposal/design/specs をレビューし、「完了後に archive へ移す」最小要件を確定する

## 2. Implementation

- [x] 2.1 `openspec/specs/version-control.md` に archive 移行 requirement を同期する
- [x] 2.2 archive 実施時の確認コマンド例（完了確認・移行後確認）を追記する

## 3. Verification

- [x] 3.1 完了済み change と未完了 change の 2 ケースで archive 判定の妥当性を確認する
- [x] 3.2 運用者向けに archive 前後の確認コマンド例をレビューする

検証メモ（2026-03-01）:

- 完了済みケース:
  - `uv run openspec status --change add-chamfer-aggregation --json` は `isComplete: true`
  - `grep -n "^- \\[ \\]" openspec/changes/add-chamfer-aggregation/tasks.md` は未完了行なし
- 未完了ケース:
  - `uv run openspec status --change stabilize-dpp-sampling --json` は `isComplete: true`
  - `grep -n "^- \\[ \\]" openspec/changes/stabilize-dpp-sampling/tasks.md` は 4 件ヒット
  - よって archive 判定には status に加えて tasks 未完了チェックが必要
- コマンド例レビュー:
  - version-control spec に「完了確認」「tasks 未完了確認」「archive 実行後確認」が揃っていることを確認
