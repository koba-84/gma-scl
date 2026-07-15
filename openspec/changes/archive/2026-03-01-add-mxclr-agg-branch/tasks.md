## 1. OpenSpec と設定更新

- [x] 1.1 MXCLR の agg 分岐要件を change specs に記述する
- [x] 1.2 MXCLR 設定ファイルに agg 引数を追加する

## 2. Loss 実装

- [x] 2.1 `src/models/loss/mxclr.py` に agg 初期化引数と値検証を追加する
- [x] 2.2 `similarity_graph` に mean/self_norm 分岐を実装する

## 3. 検証

- [x] 3.1 MXCLR 自己テストを agg 分岐・不正値ケースに対応させる
- [x] 3.2 `uv run python src/models/loss/mxclr.py` を実行して成功を確認する
