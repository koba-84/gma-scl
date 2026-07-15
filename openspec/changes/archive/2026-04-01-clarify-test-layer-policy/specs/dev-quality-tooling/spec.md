## MODIFIED Requirements

### Requirement: Parametrization must preserve a single assertion contract

Pytest parametrization MUST be used only for independent cases that share the same assertion contract. Cases that exercise different responsibilities or failure meanings MUST remain in separate test functions or modules even when they target the same feature family.

#### Scenario: Parametrize sampler variants with the same contract

- **WHEN** 開発者または coding agent が built-in sampler variants に対して同じ output hygiene や shape contract を確認する
- **THEN** `@pytest.mark.parametrize` で case を列挙してよい
- **AND** 各 case は pytest の失敗出力で独立に識別できる

#### Scenario: Do not merge different sampler responsibilities into one parametrized test

- **WHEN** sampler family が同じでも、ある case は stdout hygiene、別の case は DataModule integration や reproducibility を検証している
- **THEN** それらは同一 parametrized test にまとめない
- **AND** test 名または module 名から責務の違いが読み取れるように保つ
