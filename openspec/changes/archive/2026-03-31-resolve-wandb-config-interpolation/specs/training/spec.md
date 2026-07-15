## ADDED Requirements

### Requirement: W&B hyperparameter config must use resolved values

When training logs hyperparameters to W&B, the exported config MUST use interpolation-resolved values rather than raw Hydra `${...}` references.

#### Scenario: Log resolved trainer references to W&B

- **WHEN** 開発者または coding agent が logger 付きで hyperparameters を記録する
- **THEN** W&B に送る `contrastive` や `classification` の config には `${trainer.accelerator}` のような未解決参照が残らない
- **AND** `classification.trainer.accelerator` のような値は実際の compose 結果である `gpu` や `cpu` として記録される
