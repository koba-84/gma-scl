## Purpose

Define repository-wide static type validation workflow with mypy for Python implementation paths.

## Requirements

### Requirement: Repository-wide mypy validation scope

Python static type checks MUST cover all repository Python implementation paths (`src`, `tests`, `scripts`) through a single mypy entrypoint.

#### Scenario: Run default mypy command

- **WHEN** 開発者が `uv run mypy` を実行する
- **THEN** mypy は `src`, `tests`, `scripts` を検証対象として実行される
- **AND** 対象内の型エラーが 0 件で完了する

### Requirement: Incremental strictness with bounded Any suppression

mypy settings MUST prefer targeted suppressions over broad global suppression so that `Any` propagation is minimized while rollout remains incremental.

#### Scenario: Configure third-party import suppressions

- **WHEN** 開発者が型情報未提供ライブラリへの対処を設定する
- **THEN** 無視設定は必要最小限の範囲（モジュール単位）に限定される
- **AND** 全体の挙動を過度に弱めるグローバル抑制を追加しない
