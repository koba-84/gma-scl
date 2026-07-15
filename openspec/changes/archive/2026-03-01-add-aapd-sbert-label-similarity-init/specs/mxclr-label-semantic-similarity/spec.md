## ADDED Requirements

### Requirement: Semantic label similarity must be reflected in sample similarity graph

MXCLR は意味類似度行列を保持している場合、labels から作るサンプル間グラフを MUST その行列で重み付けして計算しなければならない。

#### Scenario: Convert labels to sample graph with semantic weighting

- **WHEN** `MXCLR.similarity_graph(labels)` が semantic 類似度有効状態で呼び出される
- **THEN** 出力 [N, N] 行列はラベル間意味類似度を反映し、有限値で 0 以上 1 以下に正規化される

### Requirement: Semantic mode must preserve existing fallback behavior

MXCLR は semantic 類似度が無効な場合、既存の labels ベース fallback 計算を MUST 維持しなければならない。

#### Scenario: Fallback path without semantic matrix

- **WHEN** `use_label_semantic_similarity=false` で `MXCLR.similarity_graph(labels)` を呼び出す
- **THEN** labels から従来と同等の fallback 類似度行列を生成する
