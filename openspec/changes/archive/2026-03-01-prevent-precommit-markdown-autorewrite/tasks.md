## 1. Markdown 自動修正の原因切り分け

- [x] 1.1 `.pre-commit-config.yaml` の Markdown 関連フック（`trailing-whitespace`、`end-of-file-fixer`、`mdformat`）の対象範囲と実行条件を整理する
- [x] 1.2 `uv run pre-commit run -a` 実行時に Markdown 差分が発生した場合のフック特定手順を `dev-quality-tooling` 仕様へ反映する

## 2. 差分混入時の標準運用を仕様化

- [x] 2.1 タスク対象外 Markdown 差分の分離ルール（別タスク化または別 change 化）を `dev-quality-tooling` 仕様へ追記する
- [x] 2.2 Python タスクの commit 前検証手順として、Markdown 差分処理後に再度 `uv run pre-commit run -a` を通す順序を明文化する

## 3. 妥当性確認

- [x] 3.1 追加した OpenSpec 変更ファイル（proposal/design/specs/tasks）の整合を確認し、`uv run openspec validate prevent-precommit-markdown-autorewrite --strict` を実行する
- [x] 3.2 検証結果と運用前提を change 内ドキュメントに反映し、適用可能状態であることを確認する
