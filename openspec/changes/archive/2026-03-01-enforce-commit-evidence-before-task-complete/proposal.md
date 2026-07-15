## Why

タスク完了チェックとコミット作成の順序が運用上曖昧なため、dirty tree が混在した状態でも「tasks は完了、commit は未作成」という不整合が再発しうる。再発防止のため、完了判定と停止条件を明確に仕様化する必要がある。

## What Changes

- エージェント完了判定に、タスク完了チェック更新前のコミット証跡確認を必須化する。
- commit ゲート未達時は tasks を完了化せず、blocked 状態として報告する運用要件を追加する。
- 混在差分時に許容される対処（対象ファイル限定ステージングまたはユーザー判断待ち）を明確化する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `agent-operation-policy`: タスク完了チェック、コミット証跡、停止報告の順序制約を追加する

## Impact

- 影響仕様: `openspec/specs/agent-operation-policy/spec.md`
- 影響運用: OpenSpec change 実装時のタスク更新フロー、完了報告フロー
