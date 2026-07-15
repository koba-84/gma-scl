## 1. Normalize Refactor

- [x] 1.1 MXCLR loss と contrastive module の正規化処理を torch.nn.functional.normalize へ統一し、重複 helper を削除する

## 2. Datamodule Refactor

- [x] 2.1 classification datamodule の train/val/test 向け dataset existence helper を 1 つに統合する

## 3. Verification And Spec Sync

- [x] 3.1 対象検証を実行し、training main spec へ内部実装方針を反映して変更を完了させる
