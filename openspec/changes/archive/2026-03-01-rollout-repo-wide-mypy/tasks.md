## 1. Scope and config

- [x] 1.1 `pyproject.toml` の mypy 対象を `src`, `tests`, `scripts` に拡張する
- [x] 1.2 `.pre-commit-config.yaml` の mypy hook 名・説明を全体スコープに更新する
- [x] 1.3 README の mypy 対象スコープ記述を更新する

## 2. Code fixes for repo-wide typing

- [x] 2.1 `src/utils` と `src/train.py` の型エラーを解消する
- [x] 2.2 `tests` 配下の型エラーを解消する
- [x] 2.3 `scripts` 配下の型エラーを解消する

## 3. Verification

- [x] 3.1 `uv run mypy` が成功することを確認する
- [x] 3.2 `uv run pre-commit run mypy --all-files` が成功することを確認する
- [x] 3.3 変更した Python ファイルに対して `uv run ruff check ...` が成功することを確認する
