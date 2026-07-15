## 1. OpenSpec Contracts

- [x] 1.1 proposal と delta specs で MXCLR agg config group 化と datamodule loader 配置方針を定義する

## 2. MXCLR Agg Config Refactor

- [x] 2.1 `configs/contrastive/model/agg/` を追加し、MXCLR の agg registry を config 注入へ置き換えて tests を更新する

## 3. Datamodule Loader Layout Refactor

- [x] 3.1 tokenized datamodule base と classification / contrastive datamodule を整理し、各 module に train/val/test loader を揃える

## 4. Verification and Spec Sync

- [x] 4.1 関連 pytest と config resolve と pre-commit を通し、main specs へ同期して change を archive する
