## ADDED Requirements

### Requirement: Ruff-based Python quality checks

The development workflow MUST use Ruff as the primary tool for Python linting and formatting.

#### Scenario: Run lint checks before commit

- **WHEN** 開発者が Python コードの品質チェックを実行する
- **THEN** `uv run ruff check .` が実行される

#### Scenario: Run formatter before commit

- **WHEN** 開発者が Python コード整形を実行する
- **THEN** `uv run ruff format .` が実行される

#### Scenario: Enforce modernized type-annotation linting

- **WHEN** 開発者が Python コードの lint を実行する
- **THEN** Ruff の `UP` ルールが有効である
- **AND** `typing.List` や `typing.Dict` などの旧記法は検出対象となる

### Requirement: Pre-commit hook consistency with Ruff

Pre-commit configuration MUST invoke Ruff hooks for Python lint and format so that local checks and manual checks stay consistent.

#### Scenario: Execute pre-commit on Python changes

- **WHEN** 開発者が Python ファイルを commit する
- **THEN** pre-commit で Ruff lint と Ruff format のフックが実行される
- **AND** 手動実行コマンドと同等のルールセットで検証される

### Requirement: Pytest coverage visibility command

The development workflow MUST provide a pytest-cov command to visualize uncovered Python paths.

#### Scenario: Run pytest with coverage report

- **WHEN** 開発者が Python テストのカバレッジを確認する
- **THEN** `uv run pytest --cov=src --cov-report=term-missing --cov-report=xml` が実行できる
- **AND** coverage データは `tmp/.coverage` と `tmp/coverage.xml` に出力される
