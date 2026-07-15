## 1. OpenSpec Artifacts

- [x] 1.1 proposal.md に AAPD 用 semantic 類似度初期化の変更目的を定義する
- [x] 1.2 design.md に初期化・保持・fallback の設計判断を記述する
- [x] 1.3 specs/training/spec.md と specs/mxclr-label-semantic-similarity/spec.md に要求を追加する

## 2. Implementation

- [x] 2.1 `src/models/loss/mxclr.py` に Sentence-BERT 依存を追加し、ラベル説明読込と類似度行列初期化を実装する
- [x] 2.2 `src/models/loss/mxclr.py` の `similarity_graph` を semantic 行列対応に更新し、fallback 経路を維持する
- [x] 2.3 `configs/contrastive/model/mxclr.yaml` に semantic 初期化用の設定キーを追加する
- [x] 2.4 `pyproject.toml` に `sentence-transformers` 依存を追加する
- [x] 2.5 `openspec/specs/training.md` と `openspec/specs/training/spec.md` に MXCLR 初期化契約の記述を追記する

## 3. Verification

- [x] 3.1 `uv run python src/models/loss/mxclr.py` を実行して自己テスト成功を確認する
- [x] 3.2 `uv run pytest tests/configs.py -q` を実行して設定 instantiate を確認する
- [x] 3.3 `uv run pytest tests/train.py -q` を実行して学習フロー回帰を確認する
- [x] 3.4 `uv run python src/train.py --cfg job --resolve contrastive/model=mxclr` で設定解決を確認する
- [x] 3.5 tasks の完了チェックを更新する
