## 1. OpenSpec Artifacts

- [x] 1.1 proposal.md に mxclr の未実装エラー化方針を定義する
- [x] 1.2 design.md に最小差分での実装方針とトレードオフを記述する
- [x] 1.3 specs/mxclr-loss/spec.md に要求とシナリオを追加する
- [x] 1.4 specs/training/spec.md に正規化処理場所（ContrastiveLitModule.\_project）を追加する

## 2. Implementation

- [x] 2.1 `src/models/loss/mxclr.py` の `MXCLR.similarity_graph` を `NotImplementedError` 送出へ変更する
- [x] 2.2 `src/models/loss/mxclr.py` の自己テストを未実装エラー検証に更新する
- [x] 2.3 `src/models/loss/mxclr.py` から埋め込み正規化処理を削除し、入力正規化は module 側前提に統一する
- [x] 2.4 `openspec/specs/training.md` に正規化処理場所を明記する
- [x] 2.5 `configs/contrastive/model/mxclr.yaml` を追加し、`MXCLR` を設定から解決可能にする

## 3. Verification

- [x] 3.1 `uv run python src/models/loss/mxclr.py` を実行し、期待どおり成功することを確認する
- [x] 3.2 `uv run python src/train.py --cfg job --resolve contrastive/model=mxclr` で設定解決できることを確認する
- [x] 3.3 change の tasks チェックボックスを完了状態へ更新する
