## Why

現在の仕様は「archive 可能条件」は定義しているものの、完了後にいつ archive するかの自律実行タイミングが曖昧です。運用ぶれをなくすため、完了判定後の自律 archive 実行を必須化します。

## What Changes

- `version-control` に、完了済み change の自律 archive 実行タイミング要件を追加する。
- `agent-operation-policy` に、tasks 完了かつ archive 前提条件成立時の archive 実行義務を追加する。
- 自律 archive を見送る条件（対象外差分混在、同名 archive 先存在など）と、その際の停止報告義務を明記する。

## Capabilities

### New Capabilities
- なし

### Modified Capabilities
- `version-control`: archive 移行のタイミング規約を追加する。
- `agent-operation-policy`: coding agent の完了後 archive 自律実行と停止報告要件を追加する。

## Impact

- 影響仕様: `openspec/specs/version-control.md`, `openspec/specs/agent-operation-policy/spec.md`
- 影響運用: change 完了時の手動 archive 依存が減り、運用が一貫する
