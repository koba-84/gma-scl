## Overview

`scripts/a.py` は prediction artifact を読み込み、`torchmetrics.classification.MultilabelF1Score` で overall Macro-F1 と帯別 Macro-F1 を計算する。頻度帯は `--boundaries` で整数列を受け取り、`(-inf, b1]`, `(b1, b2]`, ..., `(bk, inf)` の区間として割り当てる。

## Decisions

### Decision 1: 指標計算は torchmetrics に統一する

- repository 本体の classification 評価が torchmetrics を使っているため、分析スクリプト側も同じ指標実装に揃える。
- overall も帯別も `MultilabelF1Score(..., average="macro", threshold=0.5)` を使う。

### Decision 2: 頻度帯は boundaries 指定を優先する

- 研究比較では rare と frequent の境界をタスクごとに変えたい。
- そのため、ユーザー指定がある場合はそれをそのまま採用し、未指定時のみ train frequency の 4 分位から既定境界を作る。

### Decision 3: 出力には実際の frequency range と label 数を残す

- 境界だけでは tie や空帯の有無が読み取りにくい。
- 各帯ごとにラベル数と実頻度範囲を表示し、どの帯で平均されたかを明示する。
