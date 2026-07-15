## Context

pytest 公式ドキュメントでは、標準 discovery は `test_*.py` と `*_test.py` に限定される。現在のリポジトリは `python_files = ["*.py"]` により `tests/configs.py` や `tests/train.py` も test module として収集しているが、この前提は support code と test module の境界を曖昧にし、pytest 標準構成から外れている。

加えて main spec には、`tests/` 配下を接頭辞なし命名に固定する要求が残っており、今回の方針と衝突する。よって OpenSpec の契約を先に更新し、その契約に合わせてコード・ドキュメント・検証導線をまとめて切り替える。

## Goals / Non-Goals

**Goals**

- pytest discovery を標準命名へ戻す。
- test module のファイル境界と marker 境界を一致させる。
- support code を test collection ルールから切り離す。
- README と spec の実行例を実コード構成と一致させる。

**Non-Goals**

- 新しい pytest marker の導入
- `scripts/ci_pytest.sh` の fast/slow 式そのものの変更
- test 内容の大幅な書き換え

## Decisions

### Decision 1: `python_files = ["*.py"]` を削除して標準 discovery に戻す

- Rationale: pytest 公式の標準構成へ戻すことで、収集対象の判断を設定依存からファイル名規約へ移せる。

### Decision 2: 収集対象の test module は標準命名へ統一する

- `tests/configs.py` → `tests/test_configs.py`
- `tests/data_integration.py` → `tests/test_data_integration.py`
- `tests/dpp_sampler_stdout.py` → `tests/test_dpp_sampler_stdout.py`
- `tests/eval.py` → `tests/test_eval.py`
- `tests/property_based.py` → `tests/test_property_based.py`
- `tests/sweeps.py` → `tests/test_sweeps.py`
- `tests/task_wrapper.py` → `tests/test_task_wrapper.py`
- `tests/train.py` は marker 境界を揃えるため複数ファイルへ分割する

### Decision 3: support code は `tests/support/` へ移し、test module と分離する

- Rationale: helper code は test discovery の主対象ではなく、支援ライブラリとして扱うべきである。
- `tests/helpers/` を `tests/support/` へ移し、`tests.helpers.*` import を更新する。

### Decision 4: marker とファイル境界を一致させる

- `test_data_integration.py` は module-level で `integration` を付与し、fast suite から外す。
- `test_eval.py` と `test_sweeps.py` も module-level marker を明示する。
- train 系は次の 4 ファイルへ分割する。
  - `test_train_integration.py`
  - `test_train_cpu_slow.py`
  - `test_train_gpu.py`
  - `test_train_gpu_slow.py`

## Risks / Trade-offs

- [Risk] 既存の直接実行コマンドが壊れる
  - Mitigation: README と main spec の実行例を同一変更で更新する。
- [Risk] `integration` 化した `data_integration` が fast suite から外れ、回帰検知タイミングが遅くなる
  - Mitigation: suite 所属を明文化し、slow/integration suite の責務として扱う。
- [Risk] test file rename により import path や cache が乱れる
  - Mitigation: `rg`, `pytest --collect-only`, targeted pytest, `pre-commit` で検証する。

## Validation Plan

- `uv run pytest --collect-only -q`
- `uv run pytest --collect-only -m 'not slow and not integration and not gpu' -q`
- `uv run pytest --collect-only -m '(slow or integration) and not gpu' -q`
- `bash scripts/ci_pytest.sh fast`
- `bash scripts/ci_pytest.sh slow`
- `uv run pre-commit run -a`
- `uv run openspec validate standardize-pytest-discovery --type change`
- `uv run openspec validate dev-quality-tooling --type spec`
- `uv run openspec validate training --type spec`
