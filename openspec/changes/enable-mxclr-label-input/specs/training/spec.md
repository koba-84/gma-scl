## ADDED Requirements

### Requirement: MXCLR must accept labels in standard contrastive path

MXCLR は他の contrastive loss と同様に、`loss_fn(z, labels)` 形式で MUST 利用可能でなければならない。

#### Scenario: MXCLR called from model_step

- **WHEN** `ContrastiveLitModule.model_step` が `loss_fn(z, labels)` を呼び出す
- **THEN** MXCLR は labels を受け取り、内部で類似度グラフへ変換して loss を返す

### Requirement: MXCLR similarity graph fallback implementation

MXCLR の `similarity_graph` は MUST labels から有効な [N, N] 類似度行列を生成し、訓練経路で利用可能でなければならない。

#### Scenario: Build graph from labels

- **WHEN** 開発者が labels（[N, L]）を MXCLR に渡す
- **THEN** `similarity_graph` で [N, N] 行列が生成され、有限スカラー loss が返る
