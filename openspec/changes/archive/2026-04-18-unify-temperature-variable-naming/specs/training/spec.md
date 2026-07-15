## MODIFIED Requirements

### Requirement: W&B hyperparameter config must use resolved values

When training logs hyperparameters to W&B, the exported config MUST use interpolation-resolved values rather than raw Hydra `${...}` references. For the currently executing stage, the exported stage config MUST reflect the stage-effective merged runtime configuration rather than the pre-merge base config. The same export MUST include deterministic comparison aliases for contrastive/classification losses and MXCLR-family settings so dashboard columns remain stable across live logging and backfill updates.

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
- **THEN** `contrastive.model.loss_fn.graph_temperature` や `classification.model.optimizer.lr` のような leaf 値は dot-path key としても記録される
- **AND** W&B 比較列で参照する主要 hyperparameter が空欄のまま残らない

#### Scenario: Log derived loss-name aliases

- **WHEN** 開発者または coding agent が現行 config から loss 実装を一意に特定できる run を W&B へ記録する
- **THEN** `contrastive.model.loss_name` は `_target_` の module 名から導出した値として記録される
- **AND** `classification.model.loss_name` は criterion `_target_` から導出した値として記録される

#### Scenario: Log derived MXCLR agg and graph_temperature aliases

- **WHEN** 開発者または coding agent が MXCLR または MXCLR_PROTO の config を W&B へ記録する
- **THEN** `contrastive.model.loss_fn.agg_name` は `loss_fn.agg._target_` から比較用 alias として記録される
- **AND** `contrastive.model.loss_fn.graph_temperature` が config leaf に無い MXCLR_PROTO run では `graph_temperature_schedule.start` を比較用 alias として記録できる

#### Scenario: Do not derive aliases from legacy tau schedule keys

- **WHEN** 開発者または coding agent が `tau_s_schedule` のみを持つ legacy MXCLR_PROTO config を入力する
- **THEN** `contrastive.model.loss_fn.graph_temperature` alias は `tau_s_schedule` から導出されない
- **AND** `temperature` 系 canonical key を持つ config のみが温度 alias 導出対象となる

#### Scenario: Log categorical choices under stable `*_name` aliases

- **WHEN** 開発者または coding agent が implementation-backed な有限選択肢を含む config を W&B へ記録する
- **THEN** contrastive/classification loss や MXCLR agg の比較用 alias は `*_name` leaf に記録される
- **AND** structured config subtree 自体は比較 alias によって上書きされない

#### Scenario: Cover every supported categorical choice with tests

- **WHEN** 開発者または coding agent が W&B categorical alias 実装を更新する
- **THEN** `configs/contrastive/model/*.yaml` `configs/contrastive/model/agg/*.yaml` `configs/classification/loss/*.yaml` の support 対象選択肢は pytest で総当たり検証される
- **AND** 各選択肢は W&B comparison で使う canonical alias 名として記録される

#### Scenario: Keep live logging and backfill alias derivation equivalent

- **WHEN** 開発者または coding agent が runtime logging と backfill の両方で alias 補完を行う
- **THEN** 両経路は同一の alias 導出 helper を使用する
- **AND** 同じ入力 config から同じ nested alias 値が得られる

### Requirement: Contrastive temperature parameters must use canonical naming

Contrastive loss implementations and configs MUST use `temperature`-based names for public temperature parameters instead of mixed aliases such as `temp` or `tau`.

#### Scenario: Resolve single-temperature losses with canonical key

- **WHEN** 開発者が Base、MulSupCon、MSC の config を解決する
- **THEN** 公開温度キーは `temperature` である
- **AND** `temp` や `tau` は公開 config key として使われない

#### Scenario: Resolve multi-temperature losses with role-specific keys

- **WHEN** 開発者が MXCLR、MCACR、MCACRWONEG、MXCLR_PROTO の config を解決する
- **THEN** 複数温度は `instance_temperature`、`graph_temperature`、`positive_temperature`、`negative_temperature` のような役割付き `temperature` 名で公開される
- **AND** `tau_s`、`tau_s_schedule`、`temp_attract` のような旧キーは公開 config key として使われない
