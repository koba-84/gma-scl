## Why

`tests/` 配下は pytest としては動いているが、shared fixture・property test・integration test・loss regression test の責務がフラットに混在している。特に `tests/conftest.py` へ fixture が集中し、`tests/test_contrastive_losses.py` と `tests/test_property_based.py` は複数モジュールの契約を 1 ファイルで抱えているため、失敗箇所と責務境界が追いにくい。

この状態はテスト追加時の配置判断を曖昧にし、fixture 再利用と test layering policy の意図をディレクトリ構成へ反映できていない。テストを責務単位へ再配置し、shared fixture も領域別 module へ分割する。

## What Changes

- `tests/conftest.py` から domain-specific fixture を分離し、`tests/support/fixtures/` 配下へ責務別 module として移す。
- broad な `tests/test_contrastive_losses.py` を loss family ごとの regression test file へ分割する。
- broad な `tests/test_property_based.py` を target module ごとの property test file へ分割する。
- train/data 系 integration test を `tests/integration/` 以下へ再配置し、train と data の責務を分離する。
- pytest test layout について、fixture module と test directory の配置規約を main spec へ同期する。

## Capabilities

### Modified Capabilities

- `dev-quality-tooling`: pytest の shared fixture と test layering policy をディレクトリ構成へ明示的に反映する。

## Impact

- 影響コード: `tests/conftest.py`, `tests/support/fixtures/*`, `tests/losses/*`, `tests/property/*`, `tests/integration/*`
- 影響仕様: `openspec/specs/dev-quality-tooling/spec.md`
- 実行挙動への影響: なし（test layout と保守性の改善）
