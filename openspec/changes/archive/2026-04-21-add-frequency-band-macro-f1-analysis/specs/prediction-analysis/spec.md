## ADDED Requirements

### Requirement: Prediction analysis script must report frequency-band Macro-F1 for AAPD artifacts

The repository MUST provide a reproducible script that reads saved classification prediction artifacts for AAPD and reports overall Macro-F1 plus frequency-band Macro-F1 derived from train-set label frequency.

#### Scenario: Recompute AAPD Macro-F1 by frequency band

- **WHEN** 開発者または coding agent が `uv run python scripts/a.py` を実行する
- **THEN** `data/aapd/train.csv` から abstract 列を除いたラベル列の positive count が列順を保持したまま読み込まれる
- **AND** ラベルは train frequency の 4 分位に基づいて 4 つの頻度帯へ割り当てられる
- **AND** `tmp/pred/aapd/base.pt`, `tmp/pred/aapd/bce.pt`, `tmp/pred/aapd/mulsupcon.pt` の `scores` と `targets` が読み込まれる
- **AND** score は `0.5` 以上で二値化され、label-wise F1 を計算したうえで overall Macro-F1 と各頻度帯の Macro-F1 が表示される
- **AND** 出力には各頻度帯のラベル数と train frequency range が含まれる
