## Context

MXCLR は semantic 行列 `S` を使って `x S x^T` を自己正規化している。一方 MCACR は `x S x^T / (|x_i||x_j|)` を使う。ユーザー要件により MXCLR を後者へ合わせる。

## Goals / Non-Goals

**Goals:**

- MXCLR 集約を mean 集約へ変更する。
- `1-sim_mean` 以降の処理は入れない。

**Non-Goals:**

- MXCLR 損失本体の式変更。
- MCACR 実装側の変更。

## Decisions

- `similarity_graph` は `sim_mean = (x @ S @ x.T) / (count_i * count_j)` を採用する。
- `count_i` は `labels` の正例数で、0除算回避のため `clamp_min(1.0)` を使う。

## Risks / Trade-offs

- [Risk] 既存実験との数値連続性が崩れる。
  - Mitigation: change と spec に集約式の変更を明記する。
