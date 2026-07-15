## 1. MXCLR and MCACR Cleanup

- [x] 1.1 MXCLR の重複 label loader を削除し、agg dispatch を instantiate ベースの registry に置き換える
- [x] 1.2 MCACR の NPMI 読み込みを shared `label_stats` helper へ直接寄せる

## 2. Module and Datamodule Cleanup

- [x] 2.1 contrastive / finetune module の trivial helper を inline 化し、未使用の contrastive datamodule accessor を削除する

## 3. Verification and Spec Sync

- [x] 3.1 対象 self-test / config resolve を実行し、main spec へ同期して change を完了させる
