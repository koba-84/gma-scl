## 1. OpenSpec artifacts

- [x] 1.1 proposal を作成し、統合テスト対象と影響範囲を明確化する
- [x] 1.2 design を作成し、fast integration の設計方針を定義する
- [x] 1.3 training delta spec を作成し、DataModule/sampler 統合要件を追加する

## 2. Implementation

- [x] 2.1 `tests/data_integration.py` を追加する
- [x] 2.2 ClassificationDataModule 統合テスト（正常系 + num_classes 異常系）を実装する
- [x] 2.3 ContrastiveDataModule 統合テスト（shuffle/gcbs/dpp + 初期化失敗系）を実装する

## 3. Verification and review

- [x] 3.1 `uv run pytest tests/data_integration.py -q` を実行して通過確認する
- [x] 3.2 追加統合テストを code review 観点でセルフレビューし、問題があれば修正する
- [x] 3.3 `openspec/specs/training.md` に確定仕様を同期する
