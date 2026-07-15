## 1. pre-commit 設定変更

- [x] 1.1 `.pre-commit-config.yaml` の `mdformat` フックを `stages: [manual]` に変更し、commit 時の自動整形対象から除外する

## 2. ドキュメント・仕様更新

- [x] 2.1 `README.md` の品質チェック手順に、commit 時ゲートと Markdown 手動整形コマンドの使い分けを追記する
- [x] 2.2 `openspec/specs/dev-quality-tooling/spec.md` を更新し、`mdformat` manual 運用と関連要件を反映する

## 3. 妥当性確認

- [x] 3.1 `uv run openspec validate move-mdformat-to-manual-stage --strict` を実行し、change が適用可能であることを確認する
