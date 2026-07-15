## ADDED Requirements

### Requirement: Property-based testing with Hypothesis

The development workflow MUST support property-based tests with Hypothesis to validate invariants beyond example-based tests.

#### Scenario: Run Hypothesis-based tests for pure functions

- **WHEN** 開発者が純関数の境界値・組み合わせ入力を検証する
- **THEN** Hypothesis を使った pytest テストが実行できる
- **AND** テストは不変条件（例: 順列性、可換性、値域）を検証する

#### Scenario: Keep quality command documentation aligned

- **WHEN** 開発者が README の品質チェック手順を参照する
- **THEN** Hypothesis を使ったテスト実行コマンドが記載される
- **AND** 既存の Ruff / mypy / pytest-cov の手順と矛盾しない
