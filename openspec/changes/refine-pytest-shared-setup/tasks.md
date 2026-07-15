## 1. Artifacts

- [x] 1.1 Create proposal/spec/tasks for pytest shared setup refinement
- [x] 1.2 Verify artifact status is apply-ready

## 2. Implementation

- [x] 2.1 Refactor logging utils tests onto shared logger/runtime fixtures and run targeted pytest
- [x] 2.2 Refactor MXCLR and contrastive loss test setup onto shared fixtures/parametrization and run targeted pytest
- [x] 2.3 Refactor remaining data/train/eval fixture setup onto shared builders/helpers and run targeted pytest

検証メモ（2026-04-01）:

- 実行コマンド:
  - `uv run openspec status --change refine-pytest-shared-setup --json`
  - `uv run pytest tests/test_logging_utils.py -q`
  - `uv run pytest tests/test_logging_utils.py tests/test_contrastive_losses.py tests/test_property_based.py -q`
  - `uv run pytest tests/test_data_integration.py tests/test_train_integration.py tests/test_train_gpu.py tests/test_train_cpu_slow.py tests/test_eval.py -q`
  - `uv run pre-commit run -a`
- 結果:
  - change は apply-ready を確認
  - `tests/test_logging_utils.py`: `3 passed`
  - `tests/test_logging_utils.py tests/test_contrastive_losses.py tests/test_property_based.py`: `49 passed`
  - `tests/test_data_integration.py tests/test_train_integration.py tests/test_train_gpu.py tests/test_train_cpu_slow.py tests/test_eval.py`: `15 passed`
  - `pre-commit`: 全フック成功
