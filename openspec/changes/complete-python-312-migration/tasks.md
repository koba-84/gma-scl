## 1. OpenSpec and main spec updates

- [x] 1.1 change artifacts と差分 spec を作成し、`openspec/specs/python-runtime-baseline/spec.md` と `openspec/specs/dev-quality-tooling/spec.md` へ Python 3.12 基準を反映する

## 2. Repository-wide Python 3.12 alignment

- [x] 2.1 `pyproject.toml` の Python 制約と Ruff/mypy 設定を 3.12 基準へ更新する
- [x] 2.2 `uv.lock` を Python 3.12 で再生成し、lockfile 基準を 3.12 に更新する
- [x] 2.3 `.github/workflows/test.yml`, `environment.yaml`, `README.md`, `openspec/project.md` の Python 3.10 記載を 3.12 に更新する
- [x] 2.4 `scripts/test.sh` の classification override を現行 Hydra 設定と整合する形へ更新する

## 3. Verification

- [x] 3.1 `uv run pre-commit run -a` を実行し、品質ゲート通過を確認する
- [x] 3.2 `uv run pytest -m "not slow"` と必要な Python 参照検索を実行し、3.10 基準の残存が解消されたことを確認する
