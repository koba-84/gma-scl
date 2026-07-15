## Why

前回の pytest 整理で `tests/test_data_integration.py`、`tests/test_configs.py`、`tests/test_task_wrapper.py`、`tests/test_sweeps.py` の重複は減ったが、`tests/test_logging_utils.py` と MXCLR 系テストにはまだ shared fixture へ寄せられる setup が残っている。

特に `_CaptureLogger`、runtime logger/model stub、`label_descriptions.json` の生成、MXCLR の description encoder monkeypatch、Hydra compose の初期化は複数箇所で繰り返されており、pytest の fixture 共有と `tmp_path` 活用の方針からまだ改善余地がある。

## What Changes

- `tests/test_logging_utils.py` の runtime/logger setup を shared fixture へ寄せる。
- `tests/test_contrastive_losses.py` の manual tmp cleanup と残存 for-loop を pytest fixture / parametrize に整理する。
- `tests/test_property_based.py` と `tests/test_contrastive_losses.py` で共有できる MXCLR dataset / encoder stub fixture を `tests/conftest.py` に追加する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `dev-quality-tooling`: pytest shared setup reuse の対象を logging utils と MXCLR 系テストまで拡張する。

## Impact

- 影響コード: `tests/conftest.py`、`tests/test_logging_utils.py`、`tests/test_contrastive_losses.py`、`tests/test_property_based.py`
- 実行挙動への影響: なし（テストの記述整理のみ）
