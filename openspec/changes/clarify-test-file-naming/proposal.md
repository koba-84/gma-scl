## Why

`tests/test_dpp_sampler_stdout.py` だけが `test_` 接頭辞を持ち、既存テスト命名（`tests/train.py` など）と不整合になっている。pytest 設定では `python_files = ["*.py"]` を採用しており、`test_` 接頭辞は不要であるため、命名規約を明確化して統一する。

## What Changes

- `tests/test_dpp_sampler_stdout.py` を `tests/dpp_sampler_stdout.py` へリネームする。
- テストファイル命名規約として「`tests/` 配下は `<topic>.py` 形式（`test_` 接頭辞を使わない）」を仕様化する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `dev-quality-tooling`: テストファイル命名ルールを明文化し、pytest 設定と一致させる。

## Impact

- 影響コード: `tests/` 配下の命名、`openspec/specs/dev-quality-tooling/spec.md`
- 実行挙動への影響: なし（pytest の収集条件は現状維持）
