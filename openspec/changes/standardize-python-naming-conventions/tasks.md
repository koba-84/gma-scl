## 1. OpenSpec artifacts and main spec synchronization

- [x] 1.1 `openspec/specs/python-naming-conventions/spec.md` を新規追加し、関数・クラス・変数・ファイル命名と例外運用を main spec に反映する
- [x] 1.2 `openspec/specs/dev-quality-tooling/spec.md` と `openspec/specs/training/spec.md` を更新し、命名ゲートと `MXCLR` 公開名を反映する

## 2. Tooling and code alignment

- [x] 2.1 `pyproject.toml` に Ruff pep8-naming (`N`) を追加し、`MCACR_WONEG` の例外を明示する
- [x] 2.2 命名違反コード（`as F`/`as L`/`RunIf` など）を規約に合わせて修正する
- [x] 2.3 README に命名規約チェックコマンドを追記する

## 3. Verification

- [x] 3.1 `uv run pre-commit run -a` を実行し、品質ゲート通過を確認する
- [x] 3.2 `uv run ruff check . --select N` と `uv run pytest -m "not slow"` を実行し、命名規約と回帰を確認する
