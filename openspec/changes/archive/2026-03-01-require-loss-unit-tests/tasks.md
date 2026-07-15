## 1. OpenSpec仕様の追加

- [x] 1.1 `require-loss-unit-tests` proposal に対象範囲と影響範囲を確定する
- [x] 1.2 training capability の delta spec に Loss 自己テスト要件を追加する
- [x] 1.3 design で最小要件・運用制約・リスク緩和策を確定する

## 2. Loss実装ルールの反映

- [x] 2.1 `src/models/loss` 配下の各 Loss 実装に `__main__` 自己テストを実装する
- [x] 2.2 自己テストで有限スカラー出力と異常系例外の最小アサーションを満たす
- [x] 2.3 一時ファイルを使う Loss は `multi-label/tmp` 利用とクリーンアップを実装する

## 3. 実行検証と同期

- [x] 3.1 `uv run python src/models/loss/<file>.py` で各自己テストが通ることを確認する
- [x] 3.2 必要に応じて pytest 側の関連テストを更新し、重複または不足を整理する
- [x] 3.3 変更完了後に `openspec/specs/training.md` へ要件を同期する
