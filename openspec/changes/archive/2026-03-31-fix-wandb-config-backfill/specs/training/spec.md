## MODIFIED Requirements

### Requirement: W&B hyperparameter config must use resolved values

When training logs hyperparameters to W&B, the exported config MUST use interpolation-resolved values rather than raw Hydra `${...}` references. For the currently executing stage, the exported stage config MUST reflect the stage-effective merged runtime configuration rather than the pre-merge base config. The same export MUST also include flat dot-path aliases for nested leaf values so W&B comparison columns do not remain blank for logged hyperparameters.

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
