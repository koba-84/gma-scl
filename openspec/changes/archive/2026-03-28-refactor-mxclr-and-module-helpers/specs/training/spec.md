## ADDED Requirements

### Requirement: MXCLR and stage modules must avoid trivial duplicate helpers

MXCLR、contrastive module、finetune module は、shared helper が既に canonical contract を持つ処理や単純な値取り出しだけの helper を重複定義してはならない。label description 読み込みは 1 つの canonical loader に統一し、MCACR の NPMI 読み込みは shared `label_stats` helper を直接使わなければならない。

#### Scenario: Reuse canonical label and label-stats helpers

- **WHEN** 開発者または coding agent が MXCLR と MCACR の helper 実装を更新する
- **THEN** `src/models/loss/mxclr.py` の label description loader は 1 つだけ存在する
- **AND** `src/models/loss/mcacr.py` は `src/models/loss/components/label_stats.py` の `compute_npmi` を直接使う

#### Scenario: Inline trivial batch and dimension lookups

- **WHEN** 開発者または coding agent が contrastive module または finetune module の step 実装を更新する
- **THEN** batch size や projection 出力次元の単純取得は使用箇所に inline 化される
- **AND** `_batch_size_from_batch` や `_projection_output_dim` のような trivial helper を残さない

### Requirement: MXCLR agg dispatch must be registry-driven

MXCLR の agg ごとの graph builder dispatch は instantiate ベースの registry で管理しなければならない。top-level 実装は agg 文字列ごとの分岐を直接持たず、selected builder に必要な tensor 群を渡して graph を構築しなければならない。

#### Scenario: Resolve MXCLR graph builder from instantiate registry

- **WHEN** 開発者または coding agent が `src/models/loss/mxclr.py` の agg dispatch を更新する
- **THEN** agg ごとの builder 選択は instantiate ベースの registry を通じて解決される
- **AND** top-level graph builder は `agg == ...` の直列分岐を持たない
