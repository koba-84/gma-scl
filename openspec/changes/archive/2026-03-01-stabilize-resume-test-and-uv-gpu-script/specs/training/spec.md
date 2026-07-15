## ADDED Requirements

### Requirement: Resume test must align with stage checkpoint contracts

This requirement MUST run resume integration tests only on stages where checkpointing is enabled and contract-consistent with post-test checkpoint cleanup behavior.

#### Scenario: Validate resume with checkpoint artifact assertions

- **WHEN** 開発者が `tests/test_train.py::test_train_resume` で `last.ckpt` や `epoch_000.ckpt` の存在を検証する
- **THEN** 対象 stage は checkpointing が有効である
- **AND** 対象 stage の `test` は無効化され、test 後の ckpt 削除が発生しない

### Requirement: GPU smoke script must run through uv environment

This requirement SHALL launch the training entrypoint through uv run, and MUST work even when PROJECT_ROOT is unset before script execution.

#### Scenario: Run scripts/test.sh without pre-exported PROJECT_ROOT

- **WHEN** 開発者が `PROJECT_ROOT` 未設定のシェルで `bash scripts/test.sh` を実行する
- **THEN** スクリプトはリポジトリルートを `PROJECT_ROOT` として補完する
- **AND** 学習実行は `uv run python src/train.py ...` で起動される
