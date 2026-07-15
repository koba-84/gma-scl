## Context

現状の Python 品質管理は black/isort/flake8/pyupgrade が分散し、`pyproject.toml` では pytest 中心、`.pre-commit-config.yaml` で各ツールを個別設定している。Ruff は公式に flake8/isort/black/pyupgrade の置換対象を広くカバーしており、単一ツール化で実行時間と設定重複を削減できる。

## Goals / Non-Goals

**Goals:**

- Ruff を開発依存として導入し、lint/format の中心ツールを統一する。
- `pyproject.toml` と pre-commit の Python 品質設定を Ruff 基準に揃える。
- 既存コードに対する影響（ルール差分、整形差分、運用差分）を明文化する。

**Non-Goals:**

- 型チェック（mypy）や pytest-cov 以外のテスト拡張（hypothesis など）の導入は本 change では行わない。
- 既存の Markdown/YAML/Shell/Notebook 系フックの構成は変更しない。

## Decisions

1. Ruff を `dev` グループで導入する。

- 理由: 開発時のみ必要なため runtime 依存へ混入させない。
- 代替案: runtime 依存に追加。却下理由は本番実行環境の不要な肥大化。

2. Python フックを Ruff に置換する。

- 置換対象: black, isort, flake8, pyupgrade。
- 理由: 公式機能範囲と実行速度の優位性があり、同一設定面で統一できる。
- 代替案: 既存維持 + Ruff 併用。却下理由は二重チェックによる運用コスト増。

3. Ruff 設定は `pyproject.toml` に集約する。

- 理由: uv 管理の単一設定源に寄せ、pre-commit と手動実行で同一ルールを担保する。
- 代替案: pre-commit 引数ベースで都度指定。却下理由は設定の分散。

4. ルール適用は既存コードとの互換を優先して段階導入する。

- 初期は `E/F/I/UP` を主対象にし、既存の flake8 ignore を考慮して最小差分で開始する。
- 理由: 大量の一括修正を避け、変更理由を追跡しやすくする。

## Risks / Trade-offs

- [Risk] Ruff と black/isort の整形差分により一部ファイルで差分が増える → Mitigation: 一括 `ruff format` 実行後に差分をレビューし、必要なら ignore を最小追加する。
- [Risk] flake8 固有ルールとの差異で検出結果が変わる → Mitigation: 既存 ignore ポリシーを Ruff の `lint.ignore` に対応づける。
- [Risk] pre-commit フック置換直後に開発者体験が変わる → Mitigation: README に手動実行コマンドを明記し移行手順を固定化する。

## Migration Plan

1. `uv add --group dev ruff` で依存追加し lock を更新する。
2. `pyproject.toml` に Ruff 設定を追加する。
3. `.pre-commit-config.yaml` の Python 系フックを Ruff ベースに差し替える。
4. `uv run ruff check .` と `uv run ruff format --check .` を実行し、必要な差分を反映する。
5. 既存テストを実行して機能回帰がないことを確認する。

## Open Questions

- Notebook 向けの Ruff 適用を `*.ipynb` まで拡張するかは次段階で検討する。
