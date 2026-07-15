## 1. OpenSpec artifacts and main spec updates

- [x] 1.1 change artifacts（proposal/design/specs/tasks）を作成し、自律 archive 要件を定義する
- [x] 1.2 `openspec/specs/version-control.md` に完了後の自律 archive タイミング要件を反映する
- [x] 1.3 `openspec/specs/agent-operation-policy/spec.md` に自律 archive 実行要件と停止報告要件を反映する

## 2. Verification

- [x] 2.1 `uv run openspec status --change enforce-autonomous-archive-transition --json` で artifacts 完了を確認する
- [x] 2.2 `grep -n "autonomously\|自律\|archive" openspec/specs/version-control.md openspec/specs/agent-operation-policy/spec.md` で main spec 反映を確認する
