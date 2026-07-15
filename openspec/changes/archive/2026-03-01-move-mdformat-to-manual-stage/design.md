## Context

現在の pre-commit 構成では `uv run pre-commit run -a` 実行時に `mdformat` が Markdown 構文整形を行う。Python タスクの commit 前検証で Markdown 全体の整形差分が混入し、1 タスク 1 コミット運用と衝突しやすい。

一方で、末尾空白や末尾改行の修正（`trailing-whitespace`、`end-of-file-fixer`）は軽微かつ汎用的であり、commit 時に維持して問題が少ない。

## Goals / Non-Goals

**Goals:**

- commit 時 `pre-commit` ゲートから `mdformat` を分離する。
- Markdown 構文整形を必要時に明示実行できる運用を定義する。
- README と OpenSpec 仕様を実際のフック動作と一致させる。

**Non-Goals:**

- Markdown 整形自体を廃止すること。
- Ruff / mypy など Python 品質ゲートの要件を緩和すること。
- CI 全体の設計変更。

## Decisions

### Decision 1: `mdformat` を manual ステージへ移動する

- 理由: commit 時のタスク対象外差分を最小化できる。
- 代替案: `mdformat --check` を commit 時に使う。
- 不採用理由: fail は防げないため、commit 時ノイズ削減効果が限定的。

### Decision 2: `trailing-whitespace` と `end-of-file-fixer` は commit 時に維持する

- 理由: 変更は軽微で差分影響が小さく、共通品質ゲートとして有効。
- 代替案: Markdown 関連フックをすべて manual 化する。
- 不採用理由: 基本的なテキスト衛生チェックまで遅延させる価値が低い。

### Decision 3: README に manual 実行コマンドを明記する

- 理由: 運用が暗黙になると Markdown 品質が劣化するため。
- 代替案: 口頭ルールで運用する。
- 不採用理由: 再現性とオンボーディング性が低下する。

## Risks / Trade-offs

- [Risk] manual 実行を忘れて Markdown 整形が遅れる → Mitigation: README に標準コマンドを明記し、PR 前実行を推奨する。
- [Risk] commit 時にも Markdown 軽微修正が発生する → Mitigation: `trailing-whitespace`/`end-of-file-fixer` は対象外差分分離ルールを継続適用する。
- [Risk] 開発者ごとに運用差が出る → Mitigation: OpenSpec 仕様に manual 実行要件を追加し、手順を固定化する。

## Migration Plan

1. `.pre-commit-config.yaml` の `mdformat` フックに `stages: [manual]` を追加する。
2. `README.md` に Markdown 手動整形コマンドを追記し、commit 前ゲートとの差を明示する。
3. `openspec/specs/dev-quality-tooling/spec.md` を更新し、commit 時と manual 実行の責務分離を反映する。
4. `uv run openspec validate move-mdformat-to-manual-stage --strict` で change 整合性を確認する。

## Open Questions

- CI で `mdformat` を常時検証（`--check`）するかは別 change で判断する。
