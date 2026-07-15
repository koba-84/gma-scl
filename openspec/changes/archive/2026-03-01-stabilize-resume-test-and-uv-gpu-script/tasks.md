## 1. OpenSpec artifacts

- [x] 1.1 proposal に問題背景と変更方針を記載する
- [x] 1.2 design に決定事項と非対象を記載する
- [x] 1.3 specs/training/spec.md に差分要件を追加する

## 2. Implementation

- [x] 2.1 `tests/test_train.py::test_train_resume` を stage 契約準拠に修正する
- [x] 2.2 `scripts/test.sh` の実行契約を `uv run` 前提で固定する
- [x] 2.3 `tests/test_sweeps.py` から恒久 skip テストを除去する

## 3. Validation

- [x] 3.1 `uv run pytest tests/test_train.py::test_train_resume -q` を実行して結果を確認する
- [x] 3.2 `uv run pytest tests/test_sweeps.py -q --collect-only` を実行して収集成功を確認する
