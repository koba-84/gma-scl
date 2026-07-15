## Why

現行の resume 統合テストは、checkpoint 削除仕様と stage 別 checkpoint 設計を十分に反映しておらず、`last.ckpt` 不在で不安定に失敗する。あわせて GPU 実行スクリプトの実行方法を `uv run` 前提に統一し、環境差分を減らす必要がある。

## What Changes

- resume 統合テストを、checkpoint が有効な classification stage を対象にした検証へ修正する。
- checkpoint ファイルの存在確認は、test stage を無効化して ckpt 削除が発生しない条件で行うことを明確化する。
- `scripts/test.sh` の実行を `uv run python` に統一し、`PROJECT_ROOT` 未設定時の既定値を補完する。

## Capabilities

### Modified Capabilities

- training: resume テストの前提条件と GPU 実行スクリプトの実行契約を明確化する。

## Impact

- 影響コード: tests/test_train.py, scripts/test.sh
- 影響仕様: openspec/specs/training.md
