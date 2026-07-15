## 1. Wrapper 修正

- [x] 1.1 `src/utils/utils.py` の `task_wrapper` で処理成否に応じた `exit_code` 管理を追加する
- [x] 1.2 `wandb.finish(exit_code=...)` を明示呼び出しに変更し、例外再送出を維持する

## 2. テスト追加

- [x] 2.1 `task_wrapper` 正常終了時に `wandb.finish(exit_code=0)` が呼ばれるテストを追加する
- [x] 2.2 `task_wrapper` 例外終了時に `wandb.finish(exit_code=1)` が呼ばれ、例外が再送出されるテストを追加する

## 3. 検証

- [x] 3.1 追加テストを `uv run pytest` で実行し成功を確認する
- [x] 3.2 OpenSpec change のタスク進捗を更新し、apply-ready を維持する
