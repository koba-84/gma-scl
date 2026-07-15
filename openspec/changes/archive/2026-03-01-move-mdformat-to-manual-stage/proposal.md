## Why

`uv run pre-commit run -a` の commit 前ゲートで `mdformat` が Markdown 全体を整形し、Python タスクに無関係な差分が混入しやすい。コミット粒度を保ちながら品質を維持するため、Markdown 構文整形を commit 時から分離して手動実行へ移す。

## What Changes

- `.pre-commit-config.yaml` の `mdformat` フックを commit 時実行対象から外し、manual ステージでのみ実行する。
- `README.md` の品質チェック手順に、commit 前ゲートと手動 Markdown 整形コマンドの使い分けを明記する。
- `dev-quality-tooling` 仕様を更新し、Markdown 自動修正の扱いを commit 時フックと manual 整形に分離する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `dev-quality-tooling`: commit 時 pre-commit ゲートから Markdown 構文整形を分離し、manual 実行手順を標準化する。

## Impact

- pre-commit 設定: `.pre-commit-config.yaml`
- ドキュメント: `README.md`
- OpenSpec: `openspec/specs/dev-quality-tooling/spec.md`
