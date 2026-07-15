## MODIFIED Requirements

### Requirement: Prediction analysis script must report four rank-based frequency bands for AAPD artifacts

The repository MUST provide a reproducible script that reads seed-suffixed saved classification prediction artifacts for AAPD and reports overall Macro-F1 plus exactly four rank-based frequency-band Macro-F1 values derived from train-set label frequency ordering, using torchmetrics and three user-configurable rank boundaries. For each configured model, the script MUST evaluate each discovered seed artifact independently and report both seed-level values and the arithmetic mean across seeds.

#### Scenario: Recompute AAPD Macro-F1 with default rank bands

- **WHEN** 開発者または coding agent が `uv run python scripts/a.py` を実行する
- **THEN** `data/aapd/train.csv` から abstract 列を除いたラベル列の positive count が列順を保持したまま読み込まれる
- **AND** ラベルは train frequency の降順で並べられ、tie は元の列順で安定化される
- **AND** rank 境界が未指定なら、`[6, 22, 38]` が既定値として使われる
- **AND** `tmp/pred/aapd/` 配下の `bce0.pt`, `base0.pt`, `mulsupcon0.pt`, `mxclr_rank0.pt` のような `<model><seed>.pt` 形式の seed artifact がモデルごとに読み込まれる
- **AND** 各 seed artifact の `scores` と `targets` から overall Macro-F1 と各頻度帯の Macro-F1 が `torchmetrics` の multilabel F1 実装と `0.5` 閾値で計算される
- **AND** 出力には各 seed artifact の metric 値が model と seed ごとに含まれる
- **AND** モデル行の metric 値は当該モデルで検出された seed artifact ごとの metric 値の算術平均として表示される
- **AND** 出力には各モデルの `seed_count` が含まれる
- **AND** 出力には 4 つの各頻度帯の rank range、ラベル数、train frequency range が含まれる

#### Scenario: Recompute AAPD Macro-F1 with user-specified rank boundaries

- **WHEN** 開発者または coding agent が `uv run python scripts/a.py --rank-boundaries 10 20 30` を実行する
- **THEN** 頻度帯は rank `1-10`, `11-20`, `21-30`, `31-N` として構築される
- **AND** 3 個以外の rank 境界は受け付けない
- **AND** 各帯の Macro-F1 は、その帯に属するラベル列だけを対象に seed artifact ごとに `torchmetrics` で再計算される
- **AND** 出力には各 seed artifact の metric 値と seed artifact ごとの metric 値の算術平均が両方含まれる
- **AND** モデル行の metric 値は seed artifact ごとの metric 値の算術平均として表示される

#### Scenario: Print AAPD analysis rows in expected order

- **WHEN** 開発者または coding agent が `uv run python scripts/a.py` を実行する
- **THEN** モデル行は `bce`, `base`, `mulsupcon`, `mxclr_rank` の順で表示される

### Requirement: Prediction analysis scripts must report quartile frequency bands for Reuters-21578 and UKLEX artifacts

The repository MUST provide reproducible scripts that read seed-suffixed saved classification prediction artifacts for Reuters-21578 and UKLEX and report overall Macro-F1 plus exactly four label-count quartile frequency-band Macro-F1 values derived from train-set label frequency ordering, using torchmetrics. For each configured model, each script MUST evaluate each discovered seed artifact independently and report both seed-level values and the arithmetic mean across seeds.

#### Scenario: Recompute Reuters-21578 Macro-F1 with 25 percent frequency bands

- **WHEN** 開発者または coding agent が `uv run python scripts/b.py` を実行する
- **THEN** `data/reuters21578/train.csv` から abstract 列を除いたラベル列の positive count が列順を保持したまま読み込まれる
- **AND** ラベルは train frequency の降順で並べられ、tie は元の列順で安定化される
- **AND** 頻度帯はラベル数を rank 順に 4 分割し、各帯がおおむね 25% ずつになるよう構築される
- **AND** `tmp/pred/reuters21578/` 配下の `bce0.pt`, `base0.pt`, `mulsupcon0.pt`, `mxclr_rank0.pt` のような `<model><seed>.pt` 形式の seed artifact がモデルごとに読み込まれる
- **AND** 各 seed artifact の `scores` と `targets` から overall Macro-F1 と各頻度帯の Macro-F1 が `torchmetrics` の multilabel F1 実装と `0.5` 閾値で計算される
- **AND** 出力には各 seed artifact の metric 値が model と seed ごとに含まれる
- **AND** モデル行の metric 値は当該モデルで検出された seed artifact ごとの metric 値の算術平均として表示される
- **AND** 出力には各モデルの `seed_count` が含まれる
- **AND** 出力には 4 つの各頻度帯の rank range、ラベル数、train frequency range が含まれる

#### Scenario: Recompute UKLEX Macro-F1 with 25 percent frequency bands

- **WHEN** 開発者または coding agent が `uv run python scripts/c.py` を実行する
- **THEN** `data/uklex/train.csv` から abstract 列を除いたラベル列の positive count が列順を保持したまま読み込まれる
- **AND** ラベルは train frequency の降順で並べられ、tie は元の列順で安定化される
- **AND** 頻度帯はラベル数を rank 順に 4 分割し、各帯がおおむね 25% ずつになるよう構築される
- **AND** `tmp/pred/uklex/` 配下の `bce0.pt`, `base0.pt`, `mulsupcon0.pt`, `mxclr_rank0.pt` のような `<model><seed>.pt` 形式の seed artifact がモデルごとに読み込まれる
- **AND** 各 seed artifact の `scores` と `targets` から overall Macro-F1 と各頻度帯の Macro-F1 が `torchmetrics` の multilabel F1 実装と `0.5` 閾値で計算される
- **AND** 出力には各 seed artifact の metric 値が model と seed ごとに含まれる
- **AND** モデル行の metric 値は当該モデルで検出された seed artifact ごとの metric 値の算術平均として表示される
- **AND** 出力には各モデルの `seed_count` が含まれる
- **AND** 出力には 4 つの各頻度帯の rank range、ラベル数、train frequency range が含まれる
