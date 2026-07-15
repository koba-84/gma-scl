## 1. Pre-commit Hook Recovery

- [x] 1.1 interrogate を通す
  - 公開API（src 本体）の未記述メソッドに docstring を追加した。
  - interrogate は private/semiprivate/magic/property setter を除外し、データ資産・一時物・運用スクリプト・テスト（`data`, `tmp`, `scripts`, `tests`）を対象外に設定した。
  - 実行ログ: `uv run pre-commit run interrogate --all-files` が PASS（2026-03-01）。
- [x] 1.2 mdformat の依存不整合を解消する
  - mdformat フックを `rev: 1.0.0` に更新し、追加依存を `mdformat-gfm==1.0.0`, `mdformat_frontmatter==2.0.10`, `linkify-it-py` に固定した。
  - 実行ログ: `uv run pre-commit run mdformat --all-files` が PASS（2026-03-01）。
- [x] 1.3 bandit の依存欠落を解消する
  - bandit フックに `pbr` を追加して `No module named 'pbr'` を解消した。
  - 併せて `scripts/build_aapd_arxiv_label_descriptions.py` の URL 取得処理を https 限定にし、B310 を解消した。
  - 実行ログ: `uv run pre-commit run bandit --all-files` が PASS（2026-03-01）。
- [x] 1.4 shellcheck の SC2155 を修正する
  - `scripts/run.sh` で `PROJECT_ROOT` の代入と `export` を分離した。
  - 実行ログ: `uv run pre-commit run shellcheck --all-files` が PASS（2026-03-01）。
