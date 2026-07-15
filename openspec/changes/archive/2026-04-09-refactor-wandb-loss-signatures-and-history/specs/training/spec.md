## MODIFIED Requirements

### Requirement: W&B hyperparameter config must use resolved values

When training logs hyperparameters to W&B, the exported config MUST use interpolation-resolved values rather than raw Hydra `${...}` references. For the currently executing stage, the exported stage config MUST reflect the stage-effective merged runtime configuration rather than the pre-merge base config. The same export MUST include deterministic comparison aliases for contrastive/classification losses and MXCLR-family settings so dashboard columns remain stable across live logging and backfill updates.

#### Scenario: Log canonical derived aliases for loss comparison

- **WHEN** 開発者または coding agent が loss 実装を `_target_` から一意に特定できる config で run を記録する
- **THEN** `contrastive.model.loss_name` は `_target_` の module 名から導出した値として記録される
- **AND** `classification.model.loss_name` は criterion `_target_` から導出した値として記録される

#### Scenario: Log canonical MXCLR-family aliases

- **WHEN** 開発者または coding agent が MXCLR / MXCLR_PROTO 設定を W&B へ記録する
- **THEN** `contrastive.model.loss_fn.agg` は `loss_fn.agg._target_` から導出した値として記録される
- **AND** `contrastive.model.loss_fn.tau_s` は `tau_s` または `tau_s_schedule.start` から導出した値として記録される

#### Scenario: Keep live logging and backfill alias derivation equivalent

- **WHEN** 開発者または coding agent が runtime logging と backfill の両方で alias 補完を行う
- **THEN** 両経路は同一の alias 導出 helper を使用する
- **AND** 同じ入力 config から同じ nested alias 値が得られる

## ADDED Requirements

### Requirement: Contrastive loss interfaces must expose runtime-required arguments only

Contrastive loss implementations MUST expose only runtime-used inputs in public call signatures. Implementations MUST NOT accept placeholder arguments that are ignored for implementation convenience.

#### Scenario: MXCLR aggregation call passes only required label statistics

- **WHEN** 開発者または coding agent が `MXCLR.score_graph` で agg を呼び出す
- **THEN** agg 呼び出しには当該 agg が要求する label statistics のみが渡される
- **AND** 未使用統計のダミー引数（受け取り後に破棄する引数）は公開契約に含まれない

#### Scenario: MSC forward accepts only the prototype context used in runtime

- **WHEN** 開発者または coding agent が `ContrastiveLitModule` の標準経路で MSC を実行する
- **THEN** MSC の公開 forward 契約は `z`, `labels`, `prototype` の runtime 入力に限定される
- **AND** queue/key 系の未使用引数は公開契約に含まれない

### Requirement: Tokenized training encoder max length must default to 512

Tokenized datamodule settings for contrastive and classification training MUST default to `max_length=512`, and runtime datamodule constructor defaults MUST remain consistent with resolved config defaults.

#### Scenario: Resolve train config with 512 max length defaults

- **WHEN** 開発者が `uv run python src/train.py --cfg job --resolve` を実行する
- **THEN** `contrastive.data.max_length` は `512` として解決される
- **AND** `classification.data.max_length` は `512` として解決される

#### Scenario: Datamodule constructor defaults match config defaults

- **WHEN** 開発者または coding agent が datamodule を config 経由または既定引数で初期化する
- **THEN** `ClassificationDataModule` と `ContrastiveDataModule` の `max_length` 既定値は `512` である
- **AND** config とクラス既定値の不一致により解釈差が発生しない
