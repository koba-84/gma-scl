## MODIFIED Requirements

### Requirement: Python quality command documentation

Repository documentation MUST publish Python quality commands including Ruff and mypy with current verification scope.

#### Scenario: Read quality-check section

- **WHEN** 開発者が README の品質チェック手順を確認する
- **THEN** `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy` が提示される
- **AND** mypy の対象スコープ（`src`, `tests`, `scripts`）が明記される
- **AND** GitHub Actions の code-quality workflow と同じ repository 提供スクリプトまたは同等コマンドが案内される

### Requirement: Code-quality PR workflow must not require privileged changed-files integrations

The PR code-quality workflow MUST determine changed files using repository git metadata available after checkout, and MUST NOT depend on third-party integrations that can fail with repository permission errors.

#### Scenario: Run code-quality on a pull request with standard GitHub Actions token

- **WHEN** the PR code-quality workflow runs with the default repository token
- **THEN** it resolves modified files from local git history after checkout
- **AND** it does not fail with `Resource not accessible by integration` while collecting changed files
- **AND** it invokes the same repository-maintained quality entrypoint used for local reproduction
