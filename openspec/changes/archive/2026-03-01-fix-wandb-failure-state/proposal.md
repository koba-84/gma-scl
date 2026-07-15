## Why

学習処理が途中で例外終了しても、現在の実装では wandb が finished として確定される場合がある。実験管理上、失敗ジョブを成功ジョブと区別できないと再現性検証と障害分析の精度が落ちるため、終了ステータスを実際の成否に一致させる必要がある。

## What Changes

- `task_wrapper` の wandb 終了処理を修正し、例外発生時は `wandb.finish(exit_code=1)` を呼び出す。
- 正常終了時は `wandb.finish(exit_code=0)` を明示して終了ステータスを固定する。
- 失敗時の終了コード伝播を確認する単体テストを追加する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: 学習ジョブの成否に応じて wandb run state が一貫して記録される要件を追加する。

## Impact

- 変更対象コード: `src/utils/utils.py`
- 追加テスト: `tests/` 配下のユーティリティ系テスト
- 依存ライブラリ追加なし
