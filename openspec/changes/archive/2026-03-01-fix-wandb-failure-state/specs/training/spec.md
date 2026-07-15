## ADDED Requirements

### Requirement: Wandb run termination must reflect training outcome

Training 実行ラッパーは、処理成否に応じて wandb run の終了コードを明示しなければならない。正常終了時は `exit_code=0`、例外終了時は `exit_code!=0` を `wandb.finish()` に渡して run state を確定しなければならない。実装はこの終了コード契約を MUST 満たすこと。

#### Scenario: Successful training marks wandb run as finished

- **WHEN** 学習処理が例外なく完了する
- **THEN** 実装は `wandb.finish(exit_code=0)` を呼び出す

#### Scenario: Failed training marks wandb run as failed

- **WHEN** 学習処理中に例外が発生する
- **THEN** 実装は `wandb.finish(exit_code=1)` を呼び出す
- **AND** 例外は再送出され、呼び出し元に失敗が伝播する
