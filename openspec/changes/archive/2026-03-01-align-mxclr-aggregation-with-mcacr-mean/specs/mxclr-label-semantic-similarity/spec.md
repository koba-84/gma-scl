## MODIFIED Requirements

### Requirement: Semantic label similarity must be reflected in sample similarity graph

MXCLR は labels から作るサンプル間グラフを MUST `sim_mean = (y_i^T S y_j) / (|y_i||y_j|)` で計算しなければならない。`1-sim_mean` などの追加変換は行ってはならない。

#### Scenario: Convert labels to sample graph with mean aggregation

- **WHEN** `MXCLR.similarity_graph(labels)` が呼び出される
- **THEN** 出力 [N, N] はラベル間意味類似度の平均集約を反映し、有限値で 0 以上 1 以下となる
