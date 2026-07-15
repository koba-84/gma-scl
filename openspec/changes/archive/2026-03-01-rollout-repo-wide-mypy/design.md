## Context

mypy 公式ドキュメントでは、既存コードベースへの導入は段階的に対象を拡張し、型エラーを継続的に削減する運用が推奨される。加えて、未型付け依存への対応は必要最小限の抑制に留め、全体を緩めすぎない構成が推奨される。pre-commit はローカルでの一貫検証に有効だが、手動コマンドと同一スコープを維持する必要がある。

参考:

- mypy docs: Using mypy with an existing codebase
- mypy docs: Running mypy and managing imports
- pre-commit docs

## Goals / Non-Goals

**Goals:**

- `uv run mypy` のデフォルト対象を `src`, `tests`, `scripts` へ拡張する。
- 既存の Python 実装で発生する型エラーを解消し、リポジトリ全体で mypy を通す。
- pre-commit の mypy フックを全体スコープと整合させる。

**Non-Goals:**

- いきなり `strict = true` を全リポジトリへ適用する。
- 外部ライブラリの stub を広範囲に追加する。
- Python 以外の品質ゲート（shell/yaml/md）のルール変更。

## Decisions

1. mypy 対象は `src`, `tests`, `scripts` を明示する。

- 理由: 研究実装・検証コード・実行補助スクリプトの回帰を同時に検出するため。

2. 型エラー修正はモジュール群ごとに分割する（`src/utils` → `src/train.py` → `tests` → `scripts`）。

- 理由: 大規模差分を抑え、意図しない回帰を追跡しやすくするため。

3. `Any` 抑制は限定的に扱う。

- 理由: mypy docs が推奨する通り、広域抑制は型安全性を毀損しやすいため。

4. pre-commit の mypy は `uv run mypy` を呼び出す local hook で統一する。

- 理由: 仮想環境と lock に従った同一解釈を担保できるため。

## Risks / Trade-offs

- [Risk] 既存の動的実装（Hydra hparams など）で型注釈が複雑化する。
  - Mitigation: `cast` と明示的ガードで実行契約を保持しつつ型を狭める。
- [Risk] tests/scripts で一時的にエラー数が急増する。
  - Mitigation: エラーをカテゴリ別に潰し、段階ごとに `uv run mypy` を再実行する。
- [Risk] pre-commit の既存フック定義互換性問題。
  - Mitigation: 実行確認を `uv run pre-commit run mypy --all-files` で行う。

## Migration Plan

1. `pyproject.toml` の mypy `files` を `src`, `tests`, `scripts` に更新する。
2. 各モジュールで型エラーを修正し、段階ごとに mypy を再実行する。
3. `.pre-commit-config.yaml` の mypy hook 名と説明を全体スコープに更新する。
4. README の mypy スコープ記述を更新する。
5. `uv run mypy`, `uv run pre-commit run mypy --all-files`, `uv run ruff check ...` で検証する。

## Open Questions

- CI に `uv run mypy` を必須ゲートとして追加するかは次の change で決定する。
