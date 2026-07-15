## Why

property-based test の初期導入は完了したが、適用範囲は 2 関数に限定されている。次段階として適用対象を計画的に拡張し、同時に tests 配下の命名を規約に揃えて運用一貫性を維持する。

## What Changes

- property-based test 拡張対象を OpenSpec task として明示する。
- tests 配下で `test` 語を含むファイル名を機能名ベースへ揃える。
- 参照コマンドと change 文書のテストファイルパスを新命名へ同期する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- dev-quality-tooling: property-based test 拡張タスクを明示し、命名規約準拠の運用を徹底する。
- training: tests 配下の pytest ファイル命名規約への準拠を継続する。

## Impact

- テスト: tests/test_property_based.py, tests/test_task_wrapper.py の改名
- 文書: README.md, OpenSpec change 文書の実行コマンド
- 計画: openspec/changes/expand-property-based-test-coverage/tasks.md
