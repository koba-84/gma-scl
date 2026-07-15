## MODIFIED Requirements

### Requirement: W&B hyperparameter config must use resolved values

When training logs hyperparameters to W&B, the exported config MUST use interpolation-resolved values rather than raw Hydra `${...}` references. For the currently executing stage, the exported stage config MUST reflect the stage-effective merged runtime configuration rather than the pre-merge base config. The same export MUST also include flat dot-path aliases for nested leaf values so W&B comparison columns do not remain blank for logged hyperparameters. For config-derived loss selections and MXCLR family loss settings, the export MUST include stable comparison aliases when they can be inferred unambiguously from the resolved config.

#### Scenario: Log derived loss-name aliases

- **WHEN** 開発者または coding agent が現行 config から loss 実装を一意に特定できる run を W&B へ記録する
- **THEN** `contrastive.model.loss_name` や `classification.model.loss_name` は比較用 alias としても記録される
- **AND** contrastive loss 名は `_target_` の module 名から導出される

#### Scenario: Log derived MXCLR agg and tau_s aliases

- **WHEN** 開発者または coding agent が MXCLR または MXCLR_PROTO の config を W&B へ記録する
- **THEN** `contrastive.model.loss_fn.agg` は `loss_fn.agg._target_` から比較用 alias としても記録される
- **AND** `contrastive.model.loss_fn.tau_s` が config leaf に無い MXCLR_PROTO run では `tau_s_schedule.start` を比較用 alias として記録できる
