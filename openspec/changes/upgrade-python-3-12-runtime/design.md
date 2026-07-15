## Context

このリポジトリは uv を正本とする研究実装であり、同一コミットと同一設定から同一環境を再現できることが重要である。現状は `pyproject.toml` の `requires-python`、Ruff、mypy、GitHub Actions、`environment.yaml`、README のバージョン表記が Python 3.10 に固定されている一方、`uv.lock` はすでに新しい PyTorch / Lightning / Transformers 系へ解決されており、宣言下限と実利用バージョンの乖離がある。さらに `.python-version` が存在しないため、uv 実行時に作業マシン上の別 Python が選ばれやすい。

## Goals / Non-Goals

**Goals:**
- Python 3.12 をリポジトリの単一ベースラインとして宣言し、uv・CI・文書・補助マニフェストの整合性を取る。
- Python 3.12 で成立しない依存下限だけを最小限に是正し、不要な大規模依存更新は避ける。
- lockfile と新規 worktree 環境を Python 3.12 で再生成し、静的解析・テスト・依存整合性確認まで完了する。
- 変更理由と検証結果を OpenSpec artifact とコミット履歴で追跡可能にする。

**Non-Goals:**
- モデル実装、学習ロジック、ハイパーパラメータの変更
- `lightning` から `pytorch-lightning` への置換や API 移行
- 依存全体の最新化や無関係なコードリファクタリング
- 重い本番学習の実行

## Decisions

### 1. 既存 dirty tree には触れず、隔離 worktree で移行を行う

- Why: 現在のメイン worktree には本件と無関係な未コミット差分が多数あり、そこへ変更を重ねると検証結果と commit 範囲が汚染される。
- Chosen: `git worktree` でクリーンな作業木を作成し、その中で Python 3.12 環境を作る。
- Alternatives:
  - 既存 worktree 上で続行: unrelated diff と quality gate の混線リスクが高い。
  - 別 clone を作成: Git 履歴管理上は可能だが、同一ローカル repo の linked worktree の方が変更追跡が明確。

### 2. Python バージョン基準は `.python-version` と `pyproject.toml` の両方で固定する

- Why: `requires-python` だけではローカル uv 実行時に使う interpreter が固定されず、実際に 3.11 が選ばれることを確認した。
- Chosen: `requires-python = \">=3.12\"` に加え、`.python-version` を追加して uv の既定 interpreter を 3.12 に寄せる。
- Alternatives:
  - `requires-python` のみ更新: ローカル再現性が弱い。
  - `.python-version` のみ追加: パッケージメタデータが古いまま残る。

### 3. 依存下限は「Python 3.12 で成立しないもの」に限定して更新する

- Why: 研究実装では依存更新の影響面積を抑える必要がある一方、`torch>=2.0.0` などは Python 3.12 のホイール提供時期と合っていない。
- Chosen:
  - `torch` / `torchvision` は Python 3.12 向け wheel が確認できる最初の系列へ引き上げる。
  - `lightning` は Python 3.12 classifier を持つ系列へ引き上げる。
  - `transformers` は `sentence-transformers` と矛盾しない下限へ揃える。
  - それ以外は resolver と既存 lock を尊重し、下限をむやみに上げない。
- Alternatives:
  - 全依存を一括最新化: 影響が大きすぎる。
  - lockfile のみ更新して下限は放置: 将来の再解決時に Python 3.12 非対応版へ戻る余地が残る。

### 4. legacy マニフェストも整合性維持のため更新する

- Why: `requirements.txt` と `environment.yaml` は正本ではないが、現状リポジトリ内で Python 3.10 を示しており、初見の利用者に誤解を与える。
- Chosen: 正本が uv であることは維持しつつ、Python バージョンや主要依存下限だけは現在のベースラインへ合わせる。
- Alternatives:
  - legacy ファイルを未更新のままにする: ドキュメント上の矛盾が残る。

## Risks / Trade-offs

- [GPU 依存の学習 smoke が環境依存で不安定] → まず CPU/短時間で成立するエントリポイント有無を確認し、GPU 必須なら実行条件と未実施理由を明記する。
- [依存再解決で transitive dependency が予想外に上がる] → `uv lock --upgrade` 後に主要依存差分を確認し、不要な直接依存変更は行わない。
- [pre-commit が repo-wide に別問題を検出する] → 隔離 worktree で実行し、本 change 起因か既存問題かを切り分ける。
- [Python 3.12 で一部テストが不安定] → failing case を Python 3.12 起因か既存不具合かに分類して報告する。

## Migration Plan

1. OpenSpec artifact で Python 3.12 ベースライン要件を定義する。
2. 設定・依存下限・CI・補助マニフェスト・README を最小限更新する。
3. `.python-version` を追加し、uv で Python 3.12 環境へ lock/sync する。
4. `pip check`、Ruff、mypy、pytest、import smoke、可能なら軽量実行確認を行う。
5. main specs と `openspec/project.md` を同期し、品質ゲート通過後に単一 task commit を作成する。

## Open Questions

- 代表エントリポイントの smoke run を CPU のみで完結できるか、あるいは GPU 必須で未実施扱いにするか。
