## MODIFIED Requirements

### Requirement: Semantic label similarity must be reflected in sample similarity graph

MXCLR は labels から作るサンプル間グラフを MUST ラベル間意味類似度行列で重み付けして計算しなければならない。fallback 経路は持ってはならない。

#### Scenario: Convert labels to sample graph with semantic weighting

- **WHEN** `MXCLR.similarity_graph(labels)` が呼び出される
- **THEN** 出力 [N, N] 行列はラベル間意味類似度を反映し、有限値で 0 以上 1 以下に正規化される
