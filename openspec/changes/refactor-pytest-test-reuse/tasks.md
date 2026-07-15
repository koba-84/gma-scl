## 1. Artifacts

- [x] 1.1 Create proposal/spec/tasks for pytest test reuse refactor
- [x] 1.2 Verify artifact status is apply-ready

## 2. Implementation

- [x] 2.1 Refactor data integration tests onto shared synthetic dataset fixtures and run targeted pytest
- [x] 2.2 Refactor config tests onto shared Hydra/MXCLR fixtures and parametrized loss cases, then run targeted pytest
- [x] 2.3 Refactor task wrapper and sweep tests with parametrization, sync main specs, and run targeted pytest

検証メモ（2026-04-01）:

- 実行コマンド:
  - `uv run openspec status --change refactor-pytest-test-reuse --json`
  - `uv run pytest tests/test_data_integration.py -q`
  - `uv run pytest tests/test_configs.py -q`
  - `uv run pytest tests/test_task_wrapper.py tests/test_sweeps.py -q`
- 結果:
  - change は apply-ready を確認
  - `tests/test_data_integration.py`: `8 passed`
  - `tests/test_configs.py`: `7 passed`
  - `tests/test_task_wrapper.py tests/test_sweeps.py`: `2 passed, 3 skipped`
