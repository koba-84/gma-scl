## ADDED Requirements

### Requirement: Test Search Files SHALL Define GCBS Quantile Sweep Locally

This requirement SHALL define GCBS quantile sweep conditions locally within each test1-test4 search config file.

#### Scenario: Quantile sweep parameters are present in each test file

- **WHEN** 開発者が configs/hparams_search/test1.yaml から test4.yaml を確認する
- **THEN** 各ファイルに contrastive.data.gcbs.quantile と contrastive.data.gcbs.chunk_size が定義されている

### Requirement: Dedicated GCBS Quantile Grid File MUST NOT Exist

This requirement MUST remove the dedicated GCBS quantile grid config file and keep ownership in test1-test4 files.

#### Scenario: Dedicated file removed

- **WHEN** 開発者が configs/hparams_search を一覧する
- **THEN** gcbs_quantile_grid.yaml が存在しない
