# OpenSpec Agent Instructions

## 最優先

- 実装前に openspec/project.md を確認する。
- 実装前に openspec/specs/version-control.md を確認する。
- 実装前に openspec/specs/commit-message-policy/spec.md を確認する。
- 実装前に対象 change の proposal.md, design.md, tasks.md を確認する。

## 実装と進行

- OpenSpec の tasks.md に従って実装する。
- 仕様変更や機能追加は OpenSpec change artifacts を先に整備してから実装する。
- 実装完了後は main specs に同期する。

## コミット運用

- commit は openspec/specs/version-control.md のタイミング要件に従う。
- commit message は openspec/specs/commit-message-policy/spec.md に準拠する。
- Python 変更を含む commit 前に pre-commit 品質ゲートを通過させる。
- commit ゲート未達時は commit せず、停止理由と次アクションを報告する。
- タスク完了報告には対応する commit hash を含める。

## 実行環境

- Python 実行は uv run を使う。
- GPU が必要な検証はローカルマシンで実行する。
