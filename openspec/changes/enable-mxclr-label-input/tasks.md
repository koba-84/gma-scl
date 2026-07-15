## 1. OpenSpec Artifacts

- [x] 1.1 proposal.md に MXCLR 入力契約の問題と変更方針を定義する
- [x] 1.2 design.md に labels/g_soft 両対応の設計判断を記述する
- [x] 1.3 specs/training/spec.md に MXCLR 標準経路要件を追加する

## 2. Implementation

- [x] 2.1 `src/models/loss/mxclr.py` の `similarity_graph` を暫定実装する
- [x] 2.2 `src/models/loss/mxclr.py` の `forward` を labels/g_soft 両対応に更新する
- [x] 2.3 `src/models/loss/mxclr.py` の自己テストを labels 入力中心に更新する
- [x] 2.4 `openspec/specs/training.md` に MXCLR の入力契約を明記する

## 3. Verification

- [x] 3.1 `uv run python src/models/loss/mxclr.py` が成功することを確認する
- [x] 3.2 `PROJECT_ROOT=$(pwd) uv run python src/train.py --cfg job --resolve contrastive/model=mxclr` で設定解決を確認する
- [x] 3.3 `uv run pytest tests/configs.py -q` を実行して設定 instantiate を確認する（旧パス `tests/test_configs.py` は現行構成で未使用）
- [x] 3.4 tasks チェックボックスを完了状態に更新する
