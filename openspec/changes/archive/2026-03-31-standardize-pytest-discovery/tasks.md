- [x] 1. OpenSpec 契約を標準 pytest discovery 方針へ更新する
  - `proposal.md`, `design.md`, delta specs を作成し、`dev-quality-tooling` と `training` の要求変更を定義する
  - `uv run openspec validate standardize-pytest-discovery --type change` を成功させる

- [x] 2. pytest 設定と tests/support 構成を標準 discovery に合わせて再編する
  - `pyproject.toml` から `python_files = ["*.py"]` を削除する
  - tests 配下の収集対象ファイルを標準命名へ揃え、train 系を marker 境界で分割する
  - `tests/helpers/` を `tests/support/` へ移し、import path を更新する
  - `uv run pytest --collect-only -q` と targeted pytest を成功させる

- [x] 3. ドキュメントと実行導線を新構成へ同期し、ローカル品質ゲートを通す
  - `README.md` と main specs の実行例を新しい test module 名へ更新する
  - `bash scripts/ci_pytest.sh fast`
  - `bash scripts/ci_pytest.sh slow`
  - `uv run pre-commit run -a`
  - `uv run openspec validate dev-quality-tooling --type spec`
  - `uv run openspec validate training --type spec`

- [x] 4. 最終整形差分を同期し、完了済み change を archive する
  - `tests/test_eval.py` の最終 format 差分を取り込む
  - `uv run openspec status --change standardize-pytest-discovery --json` で archive 前提を確認する
  - `openspec/changes/archive/2026-03-31-standardize-pytest-discovery/` へ移動する
