## 1. Spec synchronization

- [x] 1.1 `openspec/specs/training/spec.md` と `openspec/specs/training.md` の公開クラス名を `MCACRWONEG` へ更新する
- [x] 1.2 `openspec/specs/python-naming-conventions/spec.md` と `openspec/specs/dev-quality-tooling/spec.md` から `MCACR_WONEG` 例外前提を除去する
- [x] 1.3 `openspec/specs/mcacr-woneg-loss/spec.md` と `openspec/specs/mcacr-woneg-loss.md` の公開名・target を `MCACRWONEG` へ更新する

## 2. Implementation updates

- [x] 2.1 `src/models/loss/mcacr_woneg.py` のクラス名改名と、`__init__.py`・設定・テスト参照の新クラス名更新を一括で反映する
- [x] 2.2 `pyproject.toml` の `ignore-names` から `MCACR_WONEG` を削除する

## 3. Verification

- [x] 3.1 `uv run pre-commit run -a` を実行して品質ゲート通過を確認する
- [x] 3.2 `uv run ruff check . --select N` と `PROJECT_ROOT=$(pwd) uv run python src/train.py --cfg job --resolve contrastive/model=mcacr_woneg` を実行し、命名規約と設定解決を確認する
