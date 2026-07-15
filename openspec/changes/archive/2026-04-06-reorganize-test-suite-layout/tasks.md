## 1. OpenSpec Artifacts

- [x] 1.1 proposal、design、delta spec で tests 再編方針を定義する

## 2. Core Implementation

- [x] 2.1 `tests/conftest.py` を薄くし、shared fixture を `tests/support/fixtures/` 配下へ責務別に分割する
- [x] 2.2 contrastive loss regression test を `tests/losses/` 配下の target module 単位へ再配置する
- [x] 2.3 property-based test を `tests/property/` 配下の target module 単位へ再配置する
- [x] 2.4 train/data integration test を `tests/integration/` 配下へ再配置する

## 3. Verification

- [x] 3.1 再配置後の pytest 対象群と `uv run pre-commit run -a` を通し、main spec を同期した状態で完了させる
