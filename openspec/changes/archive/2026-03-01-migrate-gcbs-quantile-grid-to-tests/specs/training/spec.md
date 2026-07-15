## MODIFIED Requirements

### Requirement: Hyperparameter Search Configurations MUST Keep Sweep Intent Co-located

This requirement SHALL keep sweep intent co-located in each hparams_search file, and MUST define GCBS quantile sweep directly in test1-test4 without a separate dedicated file.

#### Scenario: Operator selects per-test sweep file

- **WHEN** 実験担当者が hparams_search=test1 から test4 のいずれかを指定して学習を起動する
- **THEN** 指定した test 設定ファイルだけで GCBS quantile 探索条件が完結する
