## Purpose

Define local quality-gate policy based on pre-commit for individual development workflow.

## Requirements

### Requirement: Pre-commit is the mandatory local quality gate

Developers MUST run pre-commit hooks successfully before creating commits in this repository.

#### Scenario: Validate changes before commit

- **WHEN** 開発者が commit を作成する
- **THEN** `uv run pre-commit run -a` が成功している
- **AND** Python 変更では Ruff と mypy のフックが通過している

### Requirement: Pre-commit must include commit message quality gates

Pre-commit configuration MUST include commit-msg and pre-push stage hooks to validate commit message requirements.

#### Scenario: Register commit-msg gate

- **WHEN** pre-commit 設定を定義する
- **THEN** commit-msg stage に commit message 検証フックを登録する

#### Scenario: Register pre-push gate

- **WHEN** pre-commit 設定を定義する
- **THEN** pre-push stage に push 対象コミット検証フックを登録する

### Requirement: Pre-push must include branch policy gate

Pre-commit configuration MUST include a pre-push hook that validates branch naming and protected-branch destination policy.

#### Scenario: Register branch policy pre-push gate

- **WHEN** pre-commit 設定を定義する
- **THEN** pre-push stage に branch policy 検証フックを登録する
- **AND** `main` `dev` `release/*` 宛の直接 push を拒否できる
