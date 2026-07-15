## 1. Completion Gate Clarification

- [x] 1.1 `agent-operation-policy` の delta spec にタスク完了前の commit 証跡必須要件を追加する
- [x] 1.2 commit 不可時の扱いを「tasks 未完了 + blocked 報告」に統一するシナリオを追加する
- [x] 1.3 dirty tree 混在時の分離可能/不可能の分岐シナリオを追加する

## 2. Validation And Sync

- [x] 2.1 `uv run openspec validate enforce-commit-evidence-before-task-complete --strict` を実行して妥当性を確認する
- [x] 2.2 main spec へ反映が必要な差分をレビュー可能な単位でコミットする
