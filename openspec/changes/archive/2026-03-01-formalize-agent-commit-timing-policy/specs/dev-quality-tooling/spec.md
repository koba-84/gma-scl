## ADDED Requirements

### Requirement: Pre-commit and mypy are mandatory commit-time quality gates

開発者と coding agent は MUST commit 直前に pre-commit を実行し、Python 変更を含む場合は mypy 成功を確認しなければならない。

#### Scenario: Validate quality gates before commit

- **WHEN** Python 変更を含む commit を作成する
- **THEN** `uv run pre-commit run -a` が成功している
- **AND** mypy フックは `src` `tests` `scripts` を対象とした設定で成功している

#### Scenario: Block commit when quality gate fails

- **WHEN** pre-commit または mypy が失敗する
- **THEN** commit を作成してはならない
- **AND** 失敗を解消してから再実行する
