## 1. OpenSpec Artifacts

- [x] 1.1 proposal/design/specs/tasks に BERTScore_F1 agg の目的・仕様・検証方針を定義する

## 2. Core Implementation

- [x] 2.1 MXCLR 用 `BERTScore_F1` agg 実装と Hydra config を追加し、既存 `idf_chamfer` とは別選択肢として使えるようにする
- [x] 2.2 W&B alias と pytest を更新し、BERTScore_F1 の数式・instantiate・canonical agg_name を検証する

## 3. Verification And Spec Sync

- [x] 3.1 検証コマンドを成功させ、main specs へ反映した上で tasks を完了状態に更新する
