## 1. OpenSpec Contracts

- [x] 1.1 proposal / design / delta specs で loss 構成統一と pytest 移行契約を定義する

## 2. Loss Module Refactor

- [x] 2.1 `classification.py` を除く contrastive loss modules を `_compute_*` helper + wrapper 構成へ統一し、`__main__` 自己テストを削除する

## 3. Pytest Migration

- [x] 3.1 loss 単体検証を pytest へ移し、正常系・異常系・必要な Hydra instantiate をカバーする

## 4. Verification and Spec Sync

- [x] 4.1 関連 pytest と `uv run pre-commit run -a` を通し、main specs へ同期して change を完了する
