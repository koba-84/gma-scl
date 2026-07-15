## 1. configurable な頻度帯別 Macro-F1 分析へ更新する

- [x] 1.1 `scripts/a.py` を `torchmetrics` ベースへ変更し、`--boundaries` で頻度帯境界を指定可能にして、`uv run python scripts/a.py` と `uv run python scripts/a.py --boundaries 500 1000 2000` で検証する
