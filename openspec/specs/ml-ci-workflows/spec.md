## Purpose

Define GitHub Actions requirements for this ML repository so required checks stay reproducible, CPU-safe, and diagnosable.

## Requirements

### Requirement: Required PR workflows must use ML-oriented concurrency and minimal permissions

Required GitHub Actions workflows for pull requests MUST set explicit read-only baseline permissions and MUST cancel superseded in-progress PR runs for the same workflow/ref combination.

#### Scenario: Re-push to the same pull request branch

- **WHEN** a contributor pushes a newer commit to the same pull request branch
- **THEN** the previous in-progress run of the same workflow is cancelled
- **AND** the workflow token keeps only the minimum permissions required for checkout and artifact upload

### Requirement: CI environment setup must align with repository uv baseline

GitHub Actions workflows that execute Python validation MUST set up Python 3.12 and uv through official setup actions, and MUST enable uv cache keyed by repository dependency manifests.

#### Scenario: Restore cached uv dependencies

- **WHEN** a Python validation workflow starts on GitHub Actions
- **THEN** it installs Python 3.12 explicitly
- **AND** it installs uv via `astral-sh/setup-uv`
- **AND** uv cache restoration is enabled using dependency files such as `pyproject.toml` and `uv.lock`

### Requirement: Required workflows must not rely on top-level path filters for merge-critical checks

Merge-critical workflows MUST execute and decide internally whether validation is required, instead of being skipped entirely by top-level path filters.

#### Scenario: Pull request changes only documentation files

- **WHEN** a required workflow is triggered for a pull request whose changed files do not require a given validation step
- **THEN** the workflow still reaches a terminal success state
- **AND** the job may no-op after checkout and changed-files inspection
- **AND** the pull request is not left with a permanently pending required check

### Requirement: Code-quality workflow must support changed-file no-op safely

The PR code-quality workflow MUST resolve changed files from checked out git metadata and MUST skip pre-commit execution when no tracked files require validation.

#### Scenario: No relevant tracked files changed in PR

- **WHEN** the PR code-quality workflow finds no changed tracked files after checkout
- **THEN** it exits successfully without invoking `pre-commit run --files`
- **AND** it records in logs that validation was intentionally skipped

### Requirement: CPU fast test workflow must exclude GPU-marked tests

The required CPU fast test workflow MUST execute only hermetic CPU-safe tests and MUST exclude tests marked as GPU-specific.

#### Scenario: Reproduce PR fast suite on a GPU-equipped local machine

- **WHEN** a developer runs the repository-provided CPU CI command locally on a machine with visible GPUs
- **THEN** pytest executes `not slow and not gpu` semantics
- **AND** GPU-specific tests do not run merely because hardware is available

### Requirement: Slow test workflow must remain CPU-compatible and non-required

The slow GitHub Actions test workflow MUST execute only CPU-compatible slow tests and SHALL be reserved for scheduled or manual execution rather than required PR validation.

#### Scenario: Run scheduled slow suite

- **WHEN** the scheduled or manually dispatched slow workflow runs
- **THEN** it executes slow tests that exclude GPU-only markers
- **AND** the workflow is not required for routine pull request merges

### Requirement: Workflow failures must preserve diagnosable artifacts

GitHub Actions workflows that run pytest MUST upload JUnit XML and captured logs even when tests fail.

#### Scenario: Fast suite fails in CI

- **WHEN** a pytest job fails in GitHub Actions
- **THEN** the workflow uploads its JUnit XML and text logs as artifacts with short retention
- **AND** artifact upload runs under `if: always()`
