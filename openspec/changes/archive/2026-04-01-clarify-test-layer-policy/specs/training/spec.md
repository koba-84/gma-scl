## MODIFIED Requirements

### Requirement: Sampler runtime output hygiene

Repo-owned sampler runtime paths SHALL NOT emit informational stdout during normal iteration. When a sampler depends on a third-party backend that emits constructor noise, the implementation MUST suppress that output before control returns to the training loop.

#### Scenario: DPP sampler initialization does not print backend info lines

- **WHEN** DPP sampler iterates and constructs `FiniteDPP` using `L_gram_factor`
- **THEN** informational constructor prints from the third-party library are not emitted to standard output

#### Scenario: Repo-owned sampler iteration remains stdout-clean

- **WHEN** 開発者または coding agent が GCBS または DPP sampler の最小 iteration path を pytest で実行する
- **THEN** sampler runtime は標準出力へ不要な情報を出さない
- **AND** sampler 切替や batch shape の統合確認は別の integration test module が担う

### Requirement: Layered pytest coverage for training responsibilities

Training-related pytest coverage MUST keep responsibility boundaries explicit across property-based tests, targeted contract tests, integration tests, and slow or GPU runtime tests.

#### Scenario: Place a new training-related test in the correct layer

- **WHEN** 開発者または coding agent が training/data/sampler/loss に関する pytest を追加または更新する
- **THEN** pure function の不変条件は property-based test module で検証する
- **AND** component 固有契約は targeted pytest module で検証する
- **AND** DataModule/sampler 切替、schema、reproducibility、stage artifact 契約は integration module で検証する
- **AND** slow または gpu 前提の train/eval 実行は dedicated slow/gpu module へ分離する

#### Scenario: Keep sampler-specific and integration contracts separate

- **WHEN** sampler に関する pytest module を設計する
- **THEN** sampler 切替や DataModule 接続の確認は integration module に置く
- **AND** stdout hygiene のような sampler 固有契約は targeted module に置く
- **AND** 両者を 1 つの test body に混在させない
