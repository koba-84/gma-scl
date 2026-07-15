## 1. Logging Fix

- [x] 1.1 stage 実効 config を `log_hyperparameters()` に渡すよう学習コードを更新する
- [x] 1.2 stage override を含む W&B config logging の回帰テストを追加する
- [x] 1.3 nested config の leaf を flat alias としても W&B に記録する

## 2. Backfill

- [x] 2.1 直近 2 run の欠損 config を補完する W&B API 補助コードを追加する
- [x] 2.2 補助コードを使って対象 2 run を更新し、補完結果を確認する

## 3. Spec Sync

- [x] 3.1 変更内容を main spec に反映し、OpenSpec validate を通す
