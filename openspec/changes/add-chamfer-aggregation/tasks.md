## 1. OpenSpec Artifacts

- [x] 1.1 proposal.md に chamfer 集約追加の目的とスコープを定義する
- [x] 1.2 design.md に共通化方針と chamfer 数式定義を記述する
- [x] 1.3 specs/training/spec.md に `agg=chamfer` 要件を追加する

## 2. Core Implementation

- [x] 2.1 MXCLR/MCACR 共通で使う集約関数に `chamfer` 分岐を追加する
- [x] 2.2 MXCLR と MCACR の `agg` 許可値に `chamfer` を追加して共通関数を使用する
- [x] 2.3 loss 自己テストに `chamfer` ケースを追加する

## 3. Verification

- [x] 3.1 `uv run python src/models/loss/mxclr.py` を実行して自己テスト成功を確認する
- [x] 3.2 `uv run python src/models/loss/mcacr.py` を実行して自己テスト成功を確認する
- [x] 3.3 `PROJECT_ROOT=$(pwd) uv run python src/train.py --cfg job --resolve contrastive/model=mxclr contrastive.model.loss_fn.agg=chamfer` で設定解決を確認する
- [x] 3.4 `PROJECT_ROOT=$(pwd) uv run python src/train.py --cfg job --resolve contrastive/model=mcacr contrastive.model.loss_fn.agg=chamfer` で設定解決を確認する
- [x] 3.5 tasks チェックボックスを完了状態に更新する
