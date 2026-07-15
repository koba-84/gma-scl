## 1. Artifacts

- [x] 1.1 Create proposal/design/spec/tasks for test filename policy clarification
- [x] 1.2 Verify artifact status is apply-ready

## 2. Implementation

- [x] 2.1 Rename DPP stdout test file to non-prefix style and run targeted pytest
- [x] 2.2 Sync dev-quality-tooling main spec with the filename policy requirement

検証メモ（2026-03-02）:

- 実行コマンド:
  - `uv run pytest tests/dpp_sampler_stdout.py`
- 結果:
  - `1 passed`（リネーム後も対象テストが収集・成功することを確認）
