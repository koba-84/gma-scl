## Why

OpenSpec change の archive 移行ルールが暗黙的で、完了済み change が作業中ディレクトリに残ることがある。完了後に archive へ移す最小ルールを仕様化する。

## What Changes

- archive 実行の前提条件を「change 完了済み」に限定して明文化する。
- archive 先の命名規約と、移行後に満たすべき状態を定義する。

## Capabilities

### New Capabilities
- なし

### Modified Capabilities
- `version-control`: OpenSpec change 完了後の archive 移行 requirement を追加する

## Impact

- 影響仕様: `openspec/specs/version-control.md`
- 影響運用: change 完了後の archive オペレーション
- 実装影響候補: agent 手順と運用ドキュメント
