## 1. OpenSpec Artifacts

- [x] 1.1 proposal/design/specs を作成し常時semantic要件を定義する

## 2. Implementation

- [x] 2.1 `src/models/loss/mxclr.py` から `use_label_semantic_similarity` を削除する
- [x] 2.2 `src/models/loss/mxclr.py` の fallback 分岐を削除し semantic 経路のみにする
- [x] 2.3 `configs/contrastive/model/mxclr.yaml` から `use_label_semantic_similarity` を削除する
- [x] 2.4 main specs の training 記述を常時 semantic に更新する

## 3. Verification

- [x] 3.1 `uv run python src/models/loss/mxclr.py`
- [x] 3.2 `uv run pytest tests/configs.py -q`
- [x] 3.3 `uv run python src/train.py --cfg job --resolve contrastive/model=mxclr`
- [x] 3.4 tasks を完了更新する
