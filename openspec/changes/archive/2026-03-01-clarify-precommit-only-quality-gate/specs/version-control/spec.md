## MODIFIED Requirements

### Requirement: Topic-scoped push granularity with pre-push checks

Developers MUST push only coherent topic commits and MUST satisfy pre-commit quality checks before pushing.

#### Scenario: Push coherent topic only

- **WHEN** 開発者がリモートへ push する
- **THEN** 同一トピック change に属する commit 群のみを push し、未整理の暫定 commit を含めない

#### Scenario: Run mandatory checks before push

- **WHEN** 開発者が push 前最終確認を行う
- **THEN** `uv run pre-commit run -a` が成功している
- **AND** 追加の pytest 実行は推奨だが必須ではない
