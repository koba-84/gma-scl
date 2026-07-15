## Context

現状の `task_wrapper` は例外発生時でも `finally` で引数なし `wandb.finish()` を呼び出す。wandb 0.24.2 では `exit_code` 未指定時に 0 扱いとなるため、失敗ジョブが finished で確定される。

## Goals / Non-Goals

**Goals:**

- 学習処理の成否に応じて wandb run state を正しく反映する。
- 既存の例外再送出の挙動を維持する。
- 最小変更で回帰リスクを抑える。

**Non-Goals:**

- logger 基盤の全面改修。
- wandb 以外の logger の状態制御変更。

## Decisions

1. `task_wrapper` 内で終了コードを保持するローカル変数を導入する。

- 例外なし: `exit_code = 0`
- 例外あり: `exit_code = 1`
- finally で `wandb.finish(exit_code=exit_code)` を呼ぶ。

2. 例外は従来どおり再送出する。

- 失敗検知を上位へ伝播し、Hydra/CI の失敗判定を維持する。

3. テストは wandb モジュールをモックして `finish` 呼び出し引数を検証する。

- 外部通信や online/offline 実行に依存せず、安定して検証できる。

## Risks / Trade-offs

- [Risk] wandb API の将来変更で `finish(exit_code=...)` 契約が変わる可能性。
  → Mitigation: テストで `exit_code` 引数契約を固定し、変更時に早期検知する。
- [Risk] `task_wrapper` の戻り値初期化不備で別例外を誘発する可能性。
  → Mitigation: 現在の制御フローを維持し、終了コード管理のみ追加する。
