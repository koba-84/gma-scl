## MODIFIED Requirements

### Requirement: W&B hyperparameter config must use resolved values

When training logs hyperparameters to W&B, the exported config MUST use interpolation-resolved values rather than raw Hydra `${...}` references. For the currently executing stage, the exported stage config MUST reflect the stage-effective merged runtime configuration rather than the pre-merge base config. The same export MUST also include flat dot-path aliases for nested leaf values so W&B comparison columns do not remain blank for logged hyperparameters. For config-derived loss selections and MXCLR family loss settings, the export MUST include stable comparison aliases when they can be inferred unambiguously from the resolved config. Existing runs with missing comparison aliases MUST remain backfillable through the shared backfill helper so the same alias values can be restored after the fact.

#### Scenario: Log resolved trainer references to W&B

- **WHEN** 開発者または coding agent が logger 付きで hyperparameters を記録する
- **THEN** W&B に送る `contrastive` や `classification` の config には `${trainer.accelerator}` のような未解決参照が残らない
- **AND** `classification.trainer.accelerator` のような値は実際の compose 結果である `gpu` や `cpu` として記録される

#### Scenario: Log stage-effective merged config to W&B

- **WHEN** 開発者または coding agent が stage-local override を含む `contrastive` または `classification` stage を実行する
- **THEN** W&B に送る当該 stage の config は top-level `trainer` と stage-local `trainer` を merge した実効値を記録する
- **AND** stage 実行時に使われた `max_epochs` や optimizer/loss の override 値は空欄にならない

#### Scenario: Log flat aliases for nested hyperparameters

- **WHEN** 開発者または coding agent が nested config を W&B へ記録する
- **THEN** `contrastive.model.loss_fn.gamma` や `classification.model.optimizer.lr` のような leaf 値は dot-path key としても記録される
- **AND** W&B 比較列で参照する主要 hyperparameter が空欄のまま残らない

#### Scenario: Log derived loss-name aliases

- **WHEN** 開発者または coding agent が現行 config から loss 実装を一意に特定できる run を W&B へ記録する
- **THEN** `contrastive.model.loss_name` や `classification.model.loss_name` は比較用 alias としても記録される
- **AND** 既存 run の backfill でも同じ alias 値を補完できる

#### Scenario: Log derived MXCLR agg and tau_s aliases

- **WHEN** 開発者または coding agent が MXCLR または MXCLR_PROTO の config を W&B へ記録する
- **THEN** `contrastive.model.loss_fn.agg` は `loss_fn.agg._target_` から比較用 alias としても記録される
- **AND** `contrastive.model.loss_fn.tau_s` が config leaf に無い MXCLR_PROTO run では `tau_s_schedule.start` を比較用 alias として記録できる

## ADDED Requirements

### Requirement: Contrastive W&B epoch metrics must use a single explicit axis mapping

Contrastive epoch-aggregated loss metrics logged to W&B MUST use a single explicit `contrastive/epoch` axis mapping that does not conflict with the logger's default wildcard metric definition. The implementation MUST avoid wildcard stage mappings that also match the same metric names as the default `* -> trainer/global_step` definition.

#### Scenario: Map contrastive loss metrics to the epoch axis without wildcard overlap

- **WHEN** 開発者または coding agent が contrastive stage を W&B logger 付きで実行する
- **THEN** `contrastive/train/loss` と `contrastive/val/loss` は `contrastive/epoch` を step metric とする明示定義だけを持つ
- **AND** それらの metric は stage wildcard 定義と logger 既定 wildcard 定義の両方に同時一致しない

#### Scenario: Keep the epoch axis itself available

- **WHEN** 開発者または coding agent が contrastive stage の epoch 集約 metric を記録する
- **THEN** `contrastive/epoch` 自体は W&B 上で定義される
- **AND** `contrastive/train/loss` と `contrastive/val/loss` はその epoch 値に対して比較できる
