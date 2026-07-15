## Context

`MXCLRRank` は `MXCLR` を継承し、現在は teacher-order ranking 項として row-wise ListMLE を加算している。今回の変更では、既存の agg-based graph 構築経路や `lambda_rank` による重み付け契約を維持したまま、ranking 項だけを微分可能 Kendall τ に置換する必要がある。

## Goals / Non-Goals

**Goals:**
- `mxclr_rank` の ranking 項を `kendall_loss` へ置換し、`mxclr_loss + lambda_rank * kendall_loss` を明示する。
- Kendall 計算で teacher/student logits の row-wise 標準化と pairwise 比較を実装する。
- ranking sharpness を制御する係数 `k` を loss ctor と Hydra config から設定可能にする。
- 既存 `MXCLRRank` の agg 再利用・regularizer 加算・入力形状検証契約を維持する。

**Non-Goals:**
- `MXCLR` 本体の soft-target loss ロジック変更
- `mxclr_rank` 以外の loss 関数や sampler の変更
- 新しい agg 実装や config group の追加

## Decisions

### Decision 1: Kendall loss helper を listmle helper と分離して追加する

- `src/models/loss/components/diff_kendall_tau.py` に differentiable Kendall τ helper を追加する。
- `MXCLRRank` 側では helper 関数を呼び出すだけにして、ranking 数式の責務を分離する。

Rationale:
- ranking 数式のテストを `MXCLRRank` から独立して書ける。
- 既存 ListMLE helper を残せるため、比較実験や別 loss への影響を避けられる。

### Decision 2: `MXCLRRank` の公開契約は `lambda_rank` + `kendall_k` にする

- 合計損失は `mxclr_loss + lambda_rank * kendall_loss` を維持する。
- `lambda_rank == 0` のときは ranking 項を計算せず `MXCLR` と同値にする。
- `kendall_k` は `> 0` の scalar として検証し、tanh の鋭さを制御する。

Rationale:
- 既存の寄与係数 `lambda_rank` の意味を維持しつつ、Kendall 側の形状制御を独立設定できる。

### Decision 3: ranking 計算は対角除外の pairwise 平均で実装する

- `teacher_logits` と `student_logits` を行ごとに標準化した後、`(B, C, C)` の差分行列を作る。
- `torch.tril(..., diagonal=-1)` mask で self-pair と重複 pair を除外し、下三角だけ平均する。
- バッチ方向に平均し、loss は `-tau_d.mean()` とする。

Rationale:
- Kendall τ の符号付き整合をそのまま最適化目標にできる。
- 現在の `mxclr_rank` が採用している self-pair 除外方針と整合する。

## Risks / Trade-offs

- [Risk] `kendall_k` が大きすぎると tanh が飽和して勾配が小さくなる → Mitigation: デフォルト値を 1.0 にし、Hydra config で明示調整可能にする。
- [Risk] ListMLE からの置換で既存実験との非連続が生じる → Mitigation: OpenSpec spec に ranking 定義変更を明記し、commit message の Reproducibility に設定差分を残す。
