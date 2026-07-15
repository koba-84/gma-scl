## ADDED Requirements

### Requirement: Seed initialization must honor zero value
Training entrypoint MUST execute random seed initialization whenever `seed` is explicitly set, including `seed=0`.

#### Scenario: Seed initialization runs with zero
- **WHEN** 開発者が `uv run python src/train.py seed=0` を実行する
- **THEN** 実装は `lightning.seed_everything(0, workers=True)` を呼び出す

#### Scenario: Seed initialization is skipped only when unset
- **WHEN** 設定上 `seed` が未設定または `None` である
- **THEN** 学習開始時の seed 初期化は実行されない
