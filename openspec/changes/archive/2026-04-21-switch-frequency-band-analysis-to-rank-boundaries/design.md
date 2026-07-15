## Overview

`scripts/a.py` は train label frequency を降順に並べ、順位 1 から N の列として扱う。`--rank-boundaries 10 30` が与えられた場合、帯は rank `1-10`, `11-30`, `31-N` になる。各帯に属するラベル列だけを取り出し、`torchmetrics.classification.MultilabelF1Score` で Macro-F1 を再計算する。

## Decisions

### Decision 1: rank は frequency 降順、tie は元の列順で安定化する

- train.csv の列順は artifact の label 次元順と対応しているため、tie は列順維持が最も安全である。
- これにより rank 境界を指定したときの帯割り当てが再現可能になる。

### Decision 2: 既定帯は順位四分位にする

- ラベル数が変わってもほぼ均等な帯サイズを保てる。
- frequency 値分布の歪みではなく、順位に対する比較を既定で見られる。

### Decision 3: 出力には rank range と frequency range を両方出す

- ユーザーは順位で指定するが、帯の中で実際にどの程度の frequency を持つラベルが入ったかも確認したい。
- そのため表示には `rank=[a, b]`, `n=...`, `freq=[min, max]` を含める。
