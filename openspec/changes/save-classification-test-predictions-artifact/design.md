## Overview

classification test の各バッチで算出した sigmoid score と正解ラベルを module 内に蓄積し、test epoch 終了時に単一ファイルへ直列化して W&B artifact として upload する。

## Data Flow

1. `test_step` で mAP 用 `scores` と `targets` を detach して CPU buffer に追加する。
2. `on_test_start` で buffer を初期化する。
3. `on_test_end` で buffer を連結し、`trainer.default_root_dir` 配下へ保存する。
4. logger の `experiment` が `log_artifact` を提供する場合のみ `wandb.Artifact` を生成して file を追加し、run に紐付ける。

## Artifact Contract

- artifact type は classification test prediction 専用にする
- payload は `scores` と `targets` を含む単一ファイルとし、後段の metric 再計算に必要な tensor shape を保持する
- metadata には `num_examples`, `num_classes`, `format`, `stage` を記録する

## Validation

- module 単体テストで artifact file の中身と metadata を検証する
- train integration test で classification test 実行後に artifact が生成されることを検証する
