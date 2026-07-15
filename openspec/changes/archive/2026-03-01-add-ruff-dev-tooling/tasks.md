## 1. Dependency and config baseline

- [x] 1.1 `uv add --group dev ruff` で開発依存と lock を更新する
- [x] 1.2 `pyproject.toml` に Ruff の lint/format 設定を追加する

## 2. Quality workflow migration

- [x] 2.1 `.pre-commit-config.yaml` の Python 系フックを Ruff ベースに置換する
- [x] 2.2 既存設定との差分（ルール・整形・運用コマンド）を README に明記する

## 3. Verification

- [x] 3.1 `uv run ruff check .` を実行し、違反を解消する
- [x] 3.2 `uv run ruff format --check .` と既存テストを実行し、回帰がないことを確認する

## 4. Follow-up memo (next dev libraries)

- [x] 4.1 mypy 導入: 実行前に型不整合を検出し、研究コードの回帰を早期発見する
- [x] 4.2 pytest-cov 導入: テストで未カバーの箇所を可視化し、回帰防止の優先順位を明確化する
- [x] 4.3 hypothesis 導入: 境界値や組み合わせ入力を自動探索して、例ベース試験で漏れる不具合を拾う
