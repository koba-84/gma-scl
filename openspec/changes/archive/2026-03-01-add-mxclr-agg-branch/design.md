## Context

現状の MXCLR は similarity_graph の集約式が 1 つに固定されている。比較実験では mean 集約と自己正規化集約を同一コードパスで切り替えたい。既存契約（semantic 行列初期化、labels 入力経路、有限値出力）は維持しつつ、集約方式のみ切り替え可能にする。

## Goals / Non-Goals

**Goals:**

- MXCLR 初期化で agg を受け取り、similarity_graph を 2 方式で分岐できるようにする。
- 既存既定値の挙動を維持する（デフォルトは mean）。
- 設定ファイルと自己テストで agg 分岐を検証する。

**Non-Goals:**

- MCACR 実装の変更。
- MXCLR の損失本体（forward 式）の変更。
- 新しい外部依存の追加。

## Decisions

1. MXCLR に `agg: str = "mean"` を追加し、許可値を `{"mean", "self_norm"}` に限定する。
   理由: Hydra 設定から明示的に切り替えられ、実験条件を記録しやすい。

2. `similarity_graph` は共通で `weighted = x @ S @ x.T` を計算し、agg ごとに分岐する。

   - `mean`: `weighted / (|y_i||y_j| + eps)`
   - `self_norm`: `weighted / sqrt(max(w_ii, eps) * max(w_jj, eps))`
     理由: ラベル意味類似度行列を共通利用しつつ、集約差分だけを局所化できる。

3. `configs/contrastive/model/mxclr.yaml` に `agg` を追加し、既定値を `mean` とする。
   理由: 既存実験の再現性を崩さず、新方式を opt-in で使える。

4. `src/models/loss/mxclr.py` の自己テストに agg 分岐検証と不正値検証を追加する。
   理由: loss ファイル単体で仕様差分を素早く検証できる。

## Risks / Trade-offs

- [Risk] self_norm 分岐で分母が 0 に近いケースで数値不安定化する可能性
  Mitigation: 対角要素に `clamp_min(eps)` を適用し、最終出力を [0, 1] にクリップする。

- [Risk] 既存 spec は mean 固定記述を含むため、同期漏れがあると仕様不整合になる
  Mitigation: 本 change の spec に agg 分岐契約を追加し、実装後に main specs へ同期する。
