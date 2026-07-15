## 1. 仕様と設定

- [x] 1.1 MCACR agg 分岐要件を change specs に記述する
- [x] 1.2 `configs/contrastive/model/mcacr.yaml` に agg を追加する

## 2. 実装

- [x] 2.1 `src/models/loss/mcacr.py` に agg 初期化引数と値検証を追加する
- [x] 2.2 repulsion 類似度集約を mean/self_norm 分岐に更新する

## 3. 検証

- [x] 3.1 MCACR 自己テストに agg 分岐・不正値ケースを追加する
- [x] 3.2 `uv run python src/models/loss/mcacr.py` を実行して成功を確認する
