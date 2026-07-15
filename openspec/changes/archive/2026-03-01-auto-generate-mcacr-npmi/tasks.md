## 1. OpenSpec artifacts

- [x] 1.1 proposal を作成し、MCACR の NPMI 自動生成方針を定義する
- [x] 1.2 design を作成し、入力解決・生成ロジック・失敗条件を定義する
- [x] 1.3 specs/training/spec.md に自動生成要件と失敗シナリオを追加する

## 2. Implementation

- [x] 2.1 `src/models/loss/mcacr.py` に NPMI 直接計算処理（train.csv 読み込み）を実装する
- [x] 2.2 `MCACRLoss` の入力を `data_dir` と `dataset_name` に変更し、npy 読み書きを廃止する
- [x] 2.3 自己テストを拡張し、CSV 直計算経路と欠損時エラー経路を検証する

## 3. Verification

- [x] 3.1 `uv run python src/models/loss/mcacr.py` を実行し自己テスト成功を確認する
- [x] 3.2 `uv run pytest tests/configs.py -q` を実行し設定解決が壊れていないことを確認する
  - `tests/test_configs.py` は現行構成では存在しないため、対応する設定テスト `tests/configs.py` を実行して 3 passed を確認
