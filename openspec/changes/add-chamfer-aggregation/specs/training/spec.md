## ADDED Requirements

### Requirement: Contrastive aggregation contract supports chamfer mode
MXCLR と MCACR のラベル集約契約は、初期化引数 `agg` として `mean` `self_norm` に加えて `chamfer` を MUST サポートする。`chamfer` は各ラベルが相手ラベル集合内の最大類似度のみを参照し、方向別平均を対称平均して集約類似度を計算しなければならない。

#### Scenario: MXCLR computes chamfer similarity graph
- **WHEN** 開発者が `MXCLR(..., agg="chamfer")` を初期化し、`similarity_graph(labels)` を呼び出す
- **THEN** 実装は `S`（ラベル類似度行列）と labels を用いて chamfer 集約類似度を計算する
- **AND** 出力は有限値かつ `[0, 1]` 範囲に収まる

#### Scenario: MCACR uses chamfer similarity for repulsion weighting
- **WHEN** 開発者が `MCACRLoss(..., agg="chamfer")` で forward を実行する
- **THEN** 実装は repulsion 用類似度 `sim` を chamfer 集約で計算する
- **AND** 後段の重みは `repulse_weight=(1-sim)^beta` を適用する
