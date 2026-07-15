## Why

`uv run pre-commit run -a` 実行時に Markdown が意図せず自動修正され、Python 変更タスクのコミット前検証が不安定になる。タスク対象外の差分混入を防ぎ、OpenSpec の 1 タスク 1 コミット運用を安定させるため、原因特定と運用ルールを明確化する。

## What Changes

- pre-commit 実行で Markdown が自動修正されるケースを再現可能な形で整理する。
- フック構成（trailing-whitespace, end-of-file-fixer, mdformat など）の責務境界を明確化する。
- タスク対象外ファイルに自動修正が入った場合の標準運用（保持・別 change 化・継続手順）を定義する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `dev-quality-tooling`: pre-commit による Markdown 自動修正の取り扱いと運用手順を明文化する。

## Impact

- OpenSpec 文書: `openspec/specs/dev-quality-tooling/spec.md`
- pre-commit 運用: `uv run pre-commit run -a` 実行時の差分ハンドリング手順
- 開発フロー: Python テストタスクのコミット前検証手順
