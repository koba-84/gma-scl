## MODIFIED Requirements

### Requirement: Prediction analysis script must report configurable frequency-band Macro-F1 for AAPD artifacts

The repository MUST provide a reproducible script that reads saved classification prediction artifacts for AAPD and reports overall Macro-F1 plus frequency-band Macro-F1 derived from train-set label frequency, using torchmetrics and user-configurable frequency boundaries.

#### Scenario: Recompute AAPD Macro-F1 with default frequency bands

- **WHEN** 開発者または coding agent が `uv run python scripts/a.py` を実行する
- **THEN** `data/aapd/train.csv` から abstract 列を除いたラベル列の positive count が列順を保持したまま読み込まれる
- **AND** 頻度帯境界が未指定なら、train frequency の 4 分位境界が既定値として使われる
- **AND** `tmp/pred/aapd/base.pt`, `tmp/pred/aapd/bce.pt`, `tmp/pred/aapd/mulsupcon.pt` の `scores` と `targets` が読み込まれる
- **AND** overall Macro-F1 と各頻度帯の Macro-F1 は `torchmetrics` の multilabel F1 実装と `0.5` 閾値で計算される
- **AND** 出力には各頻度帯のラベル数と train frequency range が含まれる

#### Scenario: Recompute AAPD Macro-F1 with user-specified frequency boundaries

- **WHEN** 開発者または coding agent が `uv run python scripts/a.py --boundaries 500 1000 2000` を実行する
- **THEN** 頻度帯は `(-inf, 500]`, `(500, 1000]`, `(1000, 2000]`, `(2000, inf)` として構築される
- **AND** 各帯の Macro-F1 は、その帯に属するラベル列だけを対象に `torchmetrics` で再計算される
