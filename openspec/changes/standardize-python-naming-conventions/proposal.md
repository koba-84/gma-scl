## Why

関数名・クラス名・ファイル名・変数名の全体規約が断片的で、仕様と実装の整合確認が難しい状態です。ML 実験コードの再現性とレビュー効率を高めるため、命名規約をリポジトリ横断で明文化し、静的検証で常時 enforce する必要があります。

## What Changes

- Python 命名規約を、関数・クラス・変数・定数・モジュール/ファイル単位で OpenSpec に新規定義する。
- 既存の loss 命名仕様へ `MXCLR` の公開クラス名を明記し、仕様と現実装を一致させる。
- Ruff に pep8-naming ルールを導入し、pre-commit 経由で命名規約を自動検証する。
- 既存コードの命名違反を修正し、必要最小限のドメイン例外を仕様と設定に明示する。
- README の品質チェック手順へ命名規約検証の実行コマンドを追記する。

## Capabilities

### New Capabilities
- `python-naming-conventions`: Python 実装に対するリポジトリ共通の命名規約（関数・クラス・変数・ファイル）と例外運用を定義する。

### Modified Capabilities
- `dev-quality-tooling`: Ruff/pre-commit の品質ゲートに命名規約検証を追加する。
- `training`: contrastive loss 実装の公開クラス命名に `MXCLR` を追加し、命名契約を補完する。

## Impact

- 影響仕様: `openspec/specs/dev-quality-tooling/spec.md`, `openspec/specs/training/spec.md`, 新規 `openspec/specs/python-naming-conventions/spec.md`
- 影響コード: `pyproject.toml`, `.pre-commit-config.yaml`, 命名違反がある Python ファイル
- 影響運用: commit 前の `uv run pre-commit run -a` で命名違反が自動的にブロックされる
