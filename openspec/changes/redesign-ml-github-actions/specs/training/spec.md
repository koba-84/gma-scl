## MODIFIED Requirements

### Requirement: Structured local verification matrix for training changes

Training-related changes MUST distinguish CPU CI reproduction, CPU slow validation, and local GPU validation as separate verification tracks.

#### Scenario: Reproduce required CPU CI locally

- **WHEN** 開発者または coding agent が PR 必須の training-related CI をローカルで再現する
- **THEN** repository 提供の CPU CI 用スクリプトまたは同等コマンドを実行する
- **AND** その pytest 条件は `not slow and not gpu` を満たす

#### Scenario: Run local GPU verification

- **WHEN** 開発者または coding agent が GPU 固有の学習経路を検証する
- **THEN** GitHub hosted runner を前提にせずローカル実機または同等 GPU 環境で実行する
- **AND** `scripts/test.sh` または GPU marker を含む pytest が利用される

### Requirement: GPU-only pytest cases must be explicitly marked

Pytest cases that require visible GPUs SHALL be marked explicitly so CPU CI suites can exclude them deterministically.

#### Scenario: Add a GPU-specific train test

- **WHEN** 開発者または coding agent が GPU availability を前提とする pytest case を追加または更新する
- **THEN** その test には `gpu` marker が付与される
- **AND** CPU CI suite からは marker condition で除外できる
