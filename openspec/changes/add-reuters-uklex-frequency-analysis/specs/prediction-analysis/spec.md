## ADDED Requirements

### Requirement: Prediction analysis scripts must report quartile frequency bands for Reuters-21578 and UKLEX artifacts

The repository MUST provide reproducible scripts that read saved classification prediction artifacts for Reuters-21578 and UKLEX and report overall Macro-F1 plus exactly four label-count quartile frequency-band Macro-F1 values derived from train-set label frequency ordering, using torchmetrics.

#### Scenario: Recompute Reuters-21578 Macro-F1 with 25 percent frequency bands

- **WHEN** 開発者または coding agent が `uv run python scripts/b.py` を実行する
- **THEN** `data/reuters21578/train.csv` から abstract 列を除いたラベル列の positive count が列順を保持したまま読み込まれる
- **AND** ラベルは train frequency の降順で並べられ、tie は元の列順で安定化される
- **AND** 頻度帯はラベル数を rank 順に 4 分割し、各帯がおおむね 25% ずつになるよう構築される
- **AND** ラベル数が 4 で割り切れない場合、余りラベルは高頻度側の band から順に割り当てられる
- **AND** `tmp/pred/reuters21578/` 配下の `bce.pt`, `base.pt`, `mulsupcon.pt`, `mxclr_rank.pt` の `scores` と `targets` が読み込まれる
- **AND** overall Macro-F1 と各頻度帯の Macro-F1 は `torchmetrics` の multilabel F1 実装と `0.5` 閾値で計算される
- **AND** 出力には 4 つの各頻度帯の rank range、ラベル数、train frequency range が含まれる

#### Scenario: Recompute UKLEX Macro-F1 with 25 percent frequency bands

- **WHEN** 開発者または coding agent が `uv run python scripts/c.py` を実行する
- **THEN** `data/uklex/train.csv` から abstract 列を除いたラベル列の positive count が列順を保持したまま読み込まれる
- **AND** ラベルは train frequency の降順で並べられ、tie は元の列順で安定化される
- **AND** 頻度帯はラベル数を rank 順に 4 分割し、各帯がおおむね 25% ずつになるよう構築される
- **AND** ラベル数が 4 で割り切れない場合、余りラベルは高頻度側の band から順に割り当てられる
- **AND** `tmp/pred/uklex/` 配下の `bce.pt`, `base.pt`, `mulsupcon.pt`, `mxclr_rank.pt` の `scores` と `targets` が読み込まれる
- **AND** overall Macro-F1 と各頻度帯の Macro-F1 は `torchmetrics` の multilabel F1 実装と `0.5` 閾値で計算される
- **AND** 出力には 4 つの各頻度帯の rank range、ラベル数、train frequency range が含まれる
