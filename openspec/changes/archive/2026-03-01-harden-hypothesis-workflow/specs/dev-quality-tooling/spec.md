## ADDED Requirements

### Requirement: Hypothesis profile governance

The test workflow MUST define named Hypothesis profiles for local and CI execution so exploration intensity and runtime are controlled consistently.

#### Scenario: Load default local profile

- **WHEN** 開発者が profile 未指定で property-based test を実行する
- **THEN** local profile が読み込まれる
- **AND** local profile は開発速度を優先した設定で実行される

#### Scenario: Override profile for CI-strength exploration

- **WHEN** 開発者または CI が `--hypothesis-profile=ci` で実行する
- **THEN** ci profile が読み込まれる
- **AND** local より高い探索強度で実行される

### Requirement: Hypothesis reproducibility command guidance

Repository documentation MUST include Hypothesis seed/profile command examples for reproducing failing property-based tests.

#### Scenario: Re-run a failing example with fixed seed

- **WHEN** 開発者が property-based test の失敗を再現したい
- **THEN** README に `--hypothesis-seed` を含む再実行コマンドが記載される
- **AND** 必要に応じて `--hypothesis-profile` の併用例が示される
