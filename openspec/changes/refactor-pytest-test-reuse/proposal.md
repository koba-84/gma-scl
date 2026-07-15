## Why

`tests/test_data_integration.py`、`tests/test_configs.py`、`tests/test_task_wrapper.py`、`tests/test_sweeps.py` に pytest の共有 fixture や parametrization を使えば避けられる重複が残っている。現在は dataset 準備、Hydra 初期化、monkeypatch、ケース差分の記述が個別テストへ分散し、失敗時の粒度も粗い。

この状態はテスト追加時の保守コストを上げ、pytest が提供する fixture 共有と独立ケース可視化の利点を損なう。既存の `tests/conftest.py` には synthetic dataset helper と共通 config fixture があるため、新しい仕組みを増やすのではなく既存の共有基盤へ対象テストを寄せる。

## What Changes

- `tests/test_data_integration.py` を shared fixture / factory helper ベースへ整理する。
- `tests/test_configs.py` の重複した Hydra 初期化と MXCLR monkeypatch を fixture へ移す。
- `tests/test_task_wrapper.py` と `tests/test_sweeps.py` を `@pytest.mark.parametrize` ベースへ整理する。
- pytest テスト保守方針として「共有 setup は `conftest.py` fixture へ、独立ケース差分は parametrization へ」を仕様化する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `dev-quality-tooling`: pytest テストは共有 setup の共通化と独立ケースの parametrization を優先する。

## Impact

- 影響コード: `tests/conftest.py`、`tests/test_data_integration.py`、`tests/test_configs.py`、`tests/test_task_wrapper.py`、`tests/test_sweeps.py`
- 実行挙動への影響: なし（テストの保守性と失敗粒度のみ改善）
