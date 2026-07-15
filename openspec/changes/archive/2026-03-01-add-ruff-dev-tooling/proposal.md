## Why

開発用の静的解析と整形が複数ツールに分散しており、設定重複と実行コストが高い。Ruff を導入して lint と format を統合し、品質チェックを高速化しつつ設定の一貫性を高める。

## What Changes

- 開発依存に Ruff を追加し、uv 管理下で実行する。
- `pyproject.toml` に Ruff 設定（lint/format/対象除外/line-length）を追加する。
- pre-commit の Python 系フックを Ruff ベースへ置換し、重複する整形・import 整理・軽微な lint を統合する。
- 開発ドキュメントの品質チェック手順を Ruff 前提に更新する。
- **BREAKING**: 開発時の品質チェックコマンドと pre-commit の違反ルール集合が変更される。

## Capabilities

### New Capabilities

- `dev-quality-tooling`: 開発時の Python 品質チェック（lint/format/import 整理）を Ruff に統合する運用要件を定義する。

### Modified Capabilities

- `training`: 依存追加手順（`uv add --group dev`）を適用する範囲に Ruff 導入を明示し、開発環境整備の再現性を維持する。

## Impact

- 影響ファイル: `pyproject.toml`, `.pre-commit-config.yaml`, `README.md`（必要に応じて）
- 依存: 開発依存に `ruff` を追加
- 開発フロー: commit 前チェックと手動実行コマンドが Ruff 中心に変更
