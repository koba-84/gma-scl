## Why

MXCLR のサンプル間類似度集約が現在は自己正規化型で、MCACR のラベルペア平均集約と一致していない。比較一貫性のため、MXCLR 側も同じ mean 集約へ合わせる。

## What Changes

- `src/models/loss/mxclr.py` の `similarity_graph` を `sim_mean = (y_i^T S y_j) / (|y_i||y_j|)` へ変更する。
- `1-sim_mean` や追加重み変換は導入しない。
- OpenSpec 仕様へ集約式を明記する。

## Capabilities

### New Capabilities

- `mxclr-mcacr-mean-aggregation`: MXCLR のラベル集合集約を MCACR と同型の平均集約に統一する。

### Modified Capabilities

- `mxclr-label-semantic-similarity`: similarity_graph の集約式を mean 方式へ変更する。

## Impact

- 影響コード: `src/models/loss/mxclr.py`
- 影響仕様: `openspec/specs/training.md`, `openspec/specs/training/spec.md`
