## MODIFIED Requirements

### Requirement: Prediction analysis script must report four rank-based frequency bands for AAPD artifacts

The repository MUST provide a reproducible script that reads saved classification prediction artifacts for AAPD and reports overall Macro-F1 plus exactly four rank-based frequency-band Macro-F1 values derived from train-set label frequency ordering, using torchmetrics and three user-configurable rank boundaries.

#### Scenario: Recompute AAPD Macro-F1 with default four rank bands

- **WHEN** 開発者または coding agent が `uv run python scripts/a.py` を実行する
- **THEN** rank 境界が未指定なら、ラベル順位の 4 分位に対応する 3 境界が既定値として使われる
- **AND** 出力は 4 つの rank bands を含む

#### Scenario: Recompute AAPD Macro-F1 with explicit four rank bands

- **WHEN** 開発者または coding agent が `uv run python scripts/a.py --rank-boundaries 10 20 30` を実行する
- **THEN** 頻度帯は rank `1-10`, `11-20`, `21-30`, `31-N` として構築される
- **AND** 3 個以外の rank 境界は受け付けない
