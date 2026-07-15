## ADDED Requirements

### Requirement: Pre-push must validate branch governance policy

Pre-commit configuration MUST include a pre-push hook that validates branch naming and protected branch destination rules.

#### Scenario: Register pre-push branch governance hook

- **WHEN** pre-commit 設定を定義する
- **THEN** pre-push stage に branch policy 検証フックを登録する
- **AND** hook は `main` `dev` `release/*` 宛の直接 push を拒否する
