## Purpose

Define reproducible Python code-quality workflows for development by standardizing Ruff-based linting and formatting.
## Requirements
### Requirement: Pre-commit is the mandatory local quality gate

Developers MUST run pre-commit hooks successfully before creating commits in this repository.

#### Scenario: Validate changes before commit

- **WHEN** 開発者が commit を作成する
- **THEN** `uv run pre-commit run -a` が成功している
- **AND** Python 変更では Ruff と mypy のフックが通過している

### Requirement: Commit-time gate must block unverified Python commits

Developers and coding agents MUST NOT create Python commits before pre-commit and mypy gates pass.

#### Scenario: Block commit on failed quality checks

- **WHEN** `uv run pre-commit run -a` または mypy フックが失敗している
- **THEN** commit を作成してはならない
- **AND** 失敗要因を修正して再実行する

### Requirement: Autonomous commit must satisfy mandatory quality gate

Coding agents MUST execute autonomous Python commits only after mandatory pre-commit checks succeed.

#### Scenario: Run mandatory checks before autonomous commit

- **WHEN** coding agent が Python 変更を含む commit を自律作成する
- **THEN** `uv run pre-commit run -a` が commit 前に成功している
- **AND** pre-commit 内の Ruff / mypy フックが通過している

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

### Requirement: Python quality tooling must target the declared runtime baseline

Ruff and mypy configuration MUST target the repository Python runtime baseline so local checks, CI, and dependency metadata use the same language level.

#### Scenario: Run Ruff and mypy under the repository baseline

- **WHEN** 開発者または coding agent が `uv run ruff check .` または `uv run mypy` を実行する
- **THEN** Ruff `target-version` は `py312` である
- **AND** mypy `python_version` は `3.12` である
- **AND** `pyproject.toml` の `requires-python` と矛盾しない

### Requirement: Pre-commit hook consistency with Ruff

Pre-commit configuration MUST invoke Ruff hooks for Python lint and format so that local checks and manual checks stay consistent.

#### Scenario: Execute pre-commit on Python changes

- **WHEN** 開発者が Python ファイルを commit する
- **THEN** pre-commit で Ruff lint と Ruff format のフックが実行される
- **AND** 手動実行コマンドと同等のルールセットで検証される

### Requirement: Pre-commit hook consistency with Ruff and mypy

Pre-commit configuration MUST invoke Ruff hooks and mypy hook for Python checks so that local checks and manual checks stay consistent.

#### Scenario: Execute pre-commit on Python changes with type checks

- **WHEN** 開発者が Python ファイルを commit する
- **THEN** pre-commit で Ruff lint / Ruff format / mypy フックが実行される
- **AND** mypy フックは `uv run mypy` と同等スコープで検証される

### Requirement: Markdown rewrite attribution in pre-commit workflow

The development workflow MUST identify which pre-commit hook rewrote Markdown files before deciding how to handle generated diffs.

#### Scenario: Attribute rewrite source when Markdown diff appears

- **WHEN** `uv run pre-commit run -a` 実行後に Markdown 差分が発生する
- **THEN** 開発者または coding agent は `trailing-whitespace` `end-of-file-fixer` のいずれが差分を生成したか特定する
- **AND** `mdformat` は commit 時自動実行対象外であることを前提に運用判断を行う

### Requirement: Out-of-scope Markdown diffs must be separated from task commits

Developers and coding agents MUST separate out-of-scope Markdown rewrites from the current task commit when pre-commit auto-fixes files unrelated to the task scope.

#### Scenario: Split unrelated Markdown auto-fixes from active task

- **WHEN** `uv run pre-commit run -a` が現在タスクの対象外 Markdown を自動修正する
- **THEN** 対象外 Markdown 差分は現在タスクの commit に含めてはならない
- **AND** 差分は別タスクまたは別 OpenSpec change として扱う

### Requirement: Python task commits must re-run pre-commit after markdown diff handling

The development workflow MUST require a second pre-commit run after handling out-of-scope Markdown rewrites before creating a Python-task commit.

#### Scenario: Re-validate task scope after markdown diff separation

- **WHEN** Python タスクの検証中に対象外 Markdown 差分を分離した
- **THEN** commit 前に `uv run pre-commit run -a` を再実行する
- **AND** 再実行が成功した状態で対象タスク commit を作成する

### Requirement: Python quality command documentation

Repository documentation MUST publish Python quality commands including Ruff and mypy with current verification scope.

#### Scenario: Read quality-check section

- **WHEN** 開発者が README の品質チェック手順を確認する
- **THEN** `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy` が提示される
- **AND** mypy の対象スコープ（`src`, `tests`, `scripts`）が明記される
- **AND** GitHub Actions の code-quality workflow と同じ repository 提供スクリプトまたは同等コマンドが案内される

### Requirement: Manual Markdown formatting command guidance

Repository documentation MUST publish the manual mdformat execution command so Markdown structural formatting is reproducible outside commit-time hooks.

#### Scenario: Run mdformat manually for Markdown cleanup

- **WHEN** 開発者が Markdown 構文整形を実行する
- **THEN** `uv run pre-commit run mdformat --all-files --hook-stage manual` が案内される
- **AND** commit 時 `uv run pre-commit run -a` とは別運用であることが明記される

### Requirement: Pytest coverage visibility command

The development workflow MUST provide a pytest-cov command to visualize uncovered Python paths.

#### Scenario: Run pytest with coverage report

- **WHEN** 開発者が Python テストのカバレッジを確認する
- **THEN** `uv run pytest --cov=src --cov-report=term-missing --cov-report=xml` が実行できる
- **AND** coverage データは `tmp/.coverage` と `tmp/coverage.xml` に出力される

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

### Requirement: Pytest test file naming consistency

Test files under `tests/` SHALL use pytest standard discovery naming, and support code used by tests SHALL NOT rely on the same file discovery rule as collected test modules.

#### Scenario: Add collected test modules and support code under tests

- **WHEN** 開発者または coding agent が `tests/` 配下に collected test module または test 支援用 Python module を追加する
- **THEN** ファイル名は `test_<topic>.py` または `<topic>_test.py` 形式を使用する
- **AND** collected test module は pytest 標準 discovery と矛盾しない
- **AND** support code は collected test modules とは別の support 領域へ配置される
- **AND** support code は `python_files` の拡張設定に依存せず import される

### Requirement: Pytest shared setup reuse

Pytest test modules that need the same setup across multiple tests MUST centralize that setup in shared fixtures instead of duplicating arrange and cleanup logic per test. Domain-specific shared fixtures SHOULD live in dedicated modules under `tests/support/fixtures/`, while the root `tests/conftest.py` SHOULD stay limited to global pytest configuration and fixture-module registration.

#### Scenario: Reuse synthetic datasets and common initialization

- **WHEN** 開発者または coding agent が複数テストで同じ temporary dataset、Hydra 初期化、monkeypatch 群を必要とする pytest module を実装または更新する
- **THEN** 共有 setup は `tests/conftest.py` または `tests/support/fixtures/` 配下の pytest fixture module から再利用可能に集約される
- **AND** 個別テストはケース固有の入力差分と assertion のみを持つ
- **AND** `try/finally` による手動 cleanup や重複した初期化コードを各テストへ繰り返さない

### Requirement: Pytest test layering policy must define where each contract is checked

Pytest and self-test organization MUST separate shared integration contracts, property-level invariants, and component-specific compatibility regressions so maintainers can tell where a failure belongs. The directory layout SHOULD reflect that separation by keeping component regression tests under domain directories such as `tests/losses/`, property-based invariants under `tests/property/`, and multi-component train/data contracts under `tests/integration/`.

#### Scenario: Map a new test to the correct layer

- **WHEN** 開発者または coding agent が test を追加または整理する
- **THEN** pure function や algebraic invariant は `tests/property/` 配下の property-based test に配置する
- **AND** multi-component wiring や Hydra/DataModule/stage integration は `tests/integration/` 配下に配置する
- **AND** 特定実装だけが持つ third-party compatibility や runtime hygiene は `tests/losses/` など対象 domain の regression test として個別に保持できる

### Requirement: Parametrized case visibility

Pytest test modules with repeated assertions over independent case data MUST express those cases through parametrization so failures remain independently visible. Parametrization MUST be used only when the repeated cases exercise the same behavioral contract; distinct contracts MUST remain separate tests even if they share the same subsystem name.

#### Scenario: Report each supported case independently

- **WHEN** 開発者または coding agent が同一 test body で loss variant、command variant、success/failure branch など独立したケースを検証する
- **THEN** `@pytest.mark.parametrize` または同等の pytest 機構でケースを列挙する
- **AND** 各ケースは pytest の収集結果と失敗出力で独立した test case として識別できる
- **AND** 必要に応じて `ids` または `pytest.param(..., id=...)` でケース名を安定化する

#### Scenario: Keep distinct contracts as separate tests

- **WHEN** 開発者または coding agent が同一 subsystem に属するが assertion の意味が異なる test を整理する
- **THEN** 共通 setup は fixture に集約してよい
- **AND** third-party stdout 抑止、初期化順序エラー、数理的不変条件のような別契約は 1 本の parametrized test に無理に統合しない
- **AND** test 名や file 名は検証している contract を直接示す

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

### Requirement: Ruff naming rules must be part of mandatory quality gate

The mandatory quality gate MUST include Ruff pep8-naming validation for Python naming consistency.

#### Scenario: Enforce naming checks during pre-commit

- **WHEN** 開発者または coding agent が `uv run pre-commit run -a` を実行する
- **THEN** Ruff lint は pep8-naming (`N`) ルールを含めて実行される
- **AND** 命名違反がある場合は commit をブロックする
- **AND** 命名ルール向けの custom ignore-names を既定で持たない

### Requirement: Naming validation command guidance must be documented

Repository documentation MUST provide an explicit command for naming-rule validation.

#### Scenario: Read naming check command in documentation

- **WHEN** 開発者が README の品質チェック手順を確認する
- **THEN** `uv run ruff check . --select N` が命名規約確認コマンドとして提示される

### Requirement: Function redundancy review must use detector-assisted screening

Function redundancy review MUST separate mechanical detection from human review and SHALL run as a two-stage workflow.

#### Scenario: Screen redundancy candidates with Pylint similarities checker

- **WHEN** 開発者または coding agent が Python 関数の機能冗長性を点検する
- **THEN** `uv run pylint src tests scripts --disable=all --enable=duplicate-code --min-similarity-lines=4 --ignore-comments=y --ignore-docstrings=y --ignore-imports=y --ignore-signatures=y` を起点コマンドとして実行する
- **AND** 検出結果は削除確定ではなくレビュー候補として扱う

### Requirement: Unused-code screening must use Vulture

The development workflow MUST provide a Vulture-based command to screen unused Python functions before human review and deletion.

#### Scenario: Run Vulture from repository configuration

- **WHEN** 開発者または coding agent が未使用関数候補を点検する
- **THEN** `uv run vulture` を `pyproject.toml` の repository-managed 設定で実行できる
- **AND** vulture は dev dependency として管理される
- **AND** 検出結果は削除確定ではなく review 候補として扱う

### Requirement: Function consolidation must avoid premature abstraction

Function consolidation decisions MUST use the Rule of Three and change-propagation risk, and SHALL NOT consolidate immediately based on only two similar functions.

#### Scenario: Keep two similar functions separate when abstractions are still unstable

- **WHEN** 類似関数が2件のみで、責務差分を吸収するために新たな分岐や過剰な引数追加が必要になる
- **THEN** 開発者または coding agent は直ちに共通化しない
- **AND** 3件目の反復、または同一修正の複数箇所波及が確認されるまで監視候補として記録する

#### Scenario: Consolidate repeated logic when duplication becomes a maintenance risk

- **WHEN** 同一ロジックが3箇所以上で反復する、または同一バグ修正が複数関数へ同時波及することが確認された
- **THEN** 開発者または coding agent は共有ヘルパー化・抽出関数化・統合のいずれかを検討する
- **AND** 統合後に責務境界がより明瞭になる構造を選択する

### Requirement: Redundancy refactoring must preserve behavior

Redundancy-removal refactoring MUST preserve behavior and SHALL proceed in small steps.

#### Scenario: Preserve behavior while removing redundant functions

- **WHEN** 開発者または coding agent が冗長関数を統合または削除する
- **THEN** 統合前後で既存テストを green に保つ
- **AND** 必要に応じて対象関数の回帰テストまたは呼び出し経路の検証を追加してから削減する

### Requirement: Python quality configuration SHALL target the repository runtime baseline

Ruff and mypy configuration MUST target the same Python runtime baseline that the repository declares for uv execution.

#### Scenario: Read Python quality configuration after runtime baseline upgrade

- **WHEN** 開発者または coding agent が `pyproject.toml` の Python runtime baseline を確認する
- **THEN** `tool.ruff.target-version` と `tool.mypy.python_version` は同じ基準に揃う
- **AND** その基準は uv で実行する repository runtime と矛盾しない

### Requirement: Code-quality PR workflow must not require privileged changed-files integrations

The PR code-quality workflow MUST determine changed files using repository git metadata available after checkout, and MUST NOT depend on third-party integrations that can fail with repository permission errors.

#### Scenario: Run code-quality on a pull request with standard GitHub Actions token

- **WHEN** the PR code-quality workflow runs with the default repository token
- **THEN** it resolves modified files from local git history after checkout
- **AND** it does not fail with `Resource not accessible by integration` while collecting changed files
- **AND** it invokes the same repository-maintained quality entrypoint used for local reproduction

- **WHEN** 開発者が `pyproject.toml` の Ruff と mypy 設定を確認する
- **THEN** Ruff の `target-version` は Python 3.12 を対象としている
- **AND** mypy の `python_version` は Python 3.12 を対象としている
