## Overview

AAPD train.csv から abstract 列を除いた各ラベル列の positive count を取り、列順を保持したまま頻度ベクトルを作る。頻度帯は 4 分位で固定し、同頻度値の衝突で qcut が崩れないよう rank(method="first") を使って帯を割り当てる。

## Decisions

### Decision 1: 頻度帯は 4 分位で固定する

- ラベル数 54 に対して 4 帯なら各帯 13 から 14 ラベルとなり、長尾と高頻度の差を見やすい。
- 任意帯数の CLI 化は今回の要求外なので行わない。

### Decision 2: F1 再計算は classification test と同じ 0.5 閾値を使う

- prediction artifact には sigmoid 後 score が保存されているため、既存 test metric と整合する。
- 空テキスト補正の追加情報は artifact に含まれないため、artifact 再計算契約は保存済み score/target のみを使う。

### Decision 3: 集計は label-wise F1 を帯ごとに平均する

- Macro-F1 は各ラベルを等重みで扱う必要があるため、サンプル単位ではなくラベル単位 F1 の平均で定義する。
- 出力には overall と帯別の両方を含め、比較を一目で行える表形式にする。
