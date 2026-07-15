## 1. OpenSpec Artifacts

- [x] 1.1 proposal/design/specs/tasks に BERTScore_Precision / BERTScore_Recall agg の目的・仕様・検証方針を定義する

## 2. Core Implementation

- [x] 2.1 MXCLR 用 `BERTScore_Precision` / `BERTScore_Recall` agg 実装と Hydra config を追加し、BERTScore_F1 と同じ方向別 score を再利用できるようにする
- [x] 2.2 W&B alias と pytest を更新し、Precision/Recall の instantiate・canonical agg_name・転置関係を検証する

## 3. Verification And Spec Sync

- [x] 3.1 検証コマンドを成功させ、main specs へ反映した上で tasks を完了状態に更新する
