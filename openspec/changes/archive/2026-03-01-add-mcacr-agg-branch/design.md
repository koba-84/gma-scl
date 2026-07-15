## Context

MXCLR では agg 分岐を導入済みで、同様に MCACR でも集約方式を切り替えて比較したい。MCACR では repulse_weight の基礎となるラベル集合類似度の集約式を切り替えるのが最小変更である。

## Goals / Non-Goals

**Goals:**

- MCACR に `agg` 引数を追加し `mean/self_norm` を切り替える。
- 既定挙動は `mean` として後方の実験連続性を維持する。
- Hydra 設定と自己テストで切り替えを検証する。

**Non-Goals:**

- attraction 項の式変更。
- MCACR_WONEG の repulsion 式変更。

## Decisions

1. `MCACRLoss.__init__` に `agg: str = "mean"` を追加し、許可値を `{"mean", "self_norm"}` に限定する。
   理由: 設定経路で比較条件を明示できる。

2. repulsion 類似度計算で `weighted = labels @ npmi @ labels.T` を共通計算し、以下に分岐する。

- `mean`: `weighted / (|y_i||y_j| + eps)`
- `self_norm`: `weighted / sqrt(max(w_ii, eps) * max(w_jj, eps))`
  理由: 既存計算の差分を集約部分に限定できる。

3. `repulse_weight = (1 - sim).clamp_min(EPS).pow(beta)` の後段処理は維持する。
   理由: 既存 MCACR の温度・べき指数設計を崩さない。

## Risks / Trade-offs

- [Risk] self_norm で sim が 1 を超える場合、`1-sim` が負になる。
  Mitigation: sim を [0, 1] にクリップしてから repulse_weight を計算する。
