## MODIFIED Requirements

### Requirement: W&B hyperparameter config must use resolved values

When training logs hyperparameters to W&B, the exported config MUST use interpolation-resolved values rather than raw Hydra `${...}` references. For the currently executing stage, the exported stage config MUST reflect the stage-effective merged runtime configuration rather than the pre-merge base config. The same export MUST include deterministic comparison aliases for contrastive/classification losses and MXCLR-family settings so dashboard columns remain stable across live logging and backfill updates.

#### Scenario: Log categorical choices under stable `*_name` aliases

- **WHEN** 開発者または coding agent が implementation-backed な有限選択肢を含む config を W&B へ記録する
- **THEN** contrastive/classification loss や MXCLR agg の比較用 alias は `*_name` leaf に記録される
- **AND** structured config subtree 自体は比較 alias によって上書きされない

#### Scenario: Cover every supported categorical choice with tests

- **WHEN** 開発者または coding agent が W&B categorical alias 実装を更新する
- **THEN** `configs/contrastive/model/*.yaml` `configs/contrastive/model/agg/*.yaml` `configs/classification/loss/*.yaml` の support 対象選択肢は pytest で総当たり検証される
- **AND** 各選択肢は W&B comparison で使う canonical alias 名として記録される
