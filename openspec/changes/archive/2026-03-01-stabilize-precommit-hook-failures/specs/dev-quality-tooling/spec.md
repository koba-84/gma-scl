## ADDED Requirements

### Requirement: Pre-commit hook recovery task set

The project MUST maintain a task set for recovering failing pre-commit hooks when environment or configuration drift causes systematic failures.

#### Scenario: Define interrogate recovery task

- **WHEN** interrogate が docstring カバレッジ閾値未達で失敗している
- **THEN** docstring 補完を行い `--fail-under` を満たすタスクを定義する

#### Scenario: Define mdformat recovery task

- **WHEN** mdformat が依存不整合（例: parser rule 不整合）で失敗している
- **THEN** mdformat 関連依存の整合を取るタスクを定義する

#### Scenario: Define bandit recovery task

- **WHEN** bandit が依存欠落で起動失敗している
- **THEN** 必要依存を補完して実行可能化するタスクを定義する

#### Scenario: Define shellcheck recovery task

- **WHEN** shellcheck が既知警告（例: SC2155）で失敗している
- **THEN** 該当スクリプトを修正して警告解消するタスクを定義する
