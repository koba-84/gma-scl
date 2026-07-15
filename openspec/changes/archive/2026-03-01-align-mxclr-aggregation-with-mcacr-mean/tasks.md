## 1. OpenSpec Artifacts

- [x] 1.1 proposal/design/specs を作成して mean 集約要件を定義する

## 2. Implementation

- [x] 2.1 `src/models/loss/mxclr.py` の `similarity_graph` を mean 集約へ変更する
- [x] 2.2 main specs の training 記述に集約式を追記する

## 3. Verification

- [x] 3.1 `uv run python src/models/loss/mxclr.py`
- [x] 3.2 `uv run pytest tests/configs.py -q`
- [x] 3.3 `uv run pytest tests/train.py -q`
- [x] 3.4 `uv run pytest tests/eval.py -q`
- [x] 3.5 tasks を完了更新する
