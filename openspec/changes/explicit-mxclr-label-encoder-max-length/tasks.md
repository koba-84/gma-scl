## 1. OpenSpec Artifacts

- [x] 1.1 proposal.md に max length 明示化の目的とスコープを定義する
- [x] 1.2 design.md に引数追加と適用方針を記述する
- [x] 1.3 specs/training/spec.md に `sbert_max_length` 要件を追加する

## 2. Core Implementation

- [x] 2.1 `src/models/loss/mxclr.py` に `sbert_max_length` 引数と値検証を追加する
- [x] 2.2 SBERT encode 経路で `max_seq_length` を明示設定し、自己テストを更新する
- [x] 2.3 `configs/contrastive/model/mxclr.yaml` に `sbert_max_length` を追加する

## 3. Verification

- [x] 3.1 `uv run python src/models/loss/mxclr.py` を実行して自己テスト成功を確認する
- [x] 3.2 `PROJECT_ROOT=$(pwd) uv run python src/train.py --cfg job --resolve contrastive/model=mxclr` で設定解決を確認する
- [x] 3.3 main spec (`openspec/specs/training/spec.md`) へ要件を同期する
