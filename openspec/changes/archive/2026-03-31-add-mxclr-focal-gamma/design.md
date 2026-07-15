## Context

MXCLR は埋め込み類似度 logits に対して batch 内候補方向の `log_softmax` を取り、label 由来の soft target graph を用いた cross entropy で最適化している。これは InfoNCE を multi-label 条件付きの候補分類として書き直した形なので、classification の focal loss と同様に「モデルが既に高確信な候補」を減衰する余地がある。

## Goals / Non-Goals

**Goals:**

- MXCLR が scalar hyperparameter `gamma` を受け取り、InfoNCE の候補 cross entropy に focal-style weighting を適用できる。
- `gamma=0` では現行実装と同じ loss を返す。
- Hydra 既定設定と pytest 群で `gamma` が追跡できる。

**Non-Goals:**

- `score_graph(labels)` の定義や agg family の挙動変更。
- classification loss 側の `gamma_pos` / `gamma_neg` 契約との統合。
- focal loss の `alpha` や class-wise weighting の追加。

## Decisions

1. MXCLR の初期化引数へ `gamma: float = 0.0` を追加し、負値を禁止する。

- 理由: 既定値 0 で完全に後退互換ではなく「同一式の特例」として現行挙動を保ちつつ、実験では scalar 1 つで強度調整できる。
- 代替案: `gamma_pos` / `gamma_neg` のような複数パラメータを導入する。
  - 不採用理由: MXCLR は batch 内候補分類であり、positive/negative を別々の BCE 項として持たないため、まずは CE 解釈に自然な単一 `gamma` を採用する。

2. focal-style weight は `log_softmax(logits)` から得た候補確率 `p = exp(log_p)` に対し `(1 - p)^gamma` を候補ごとに計算し、soft target `s` と負 log likelihood の積へ直接掛ける。

- 理由: CE の各候補項に対して難易度依存の減衰を入れると、soft target 分布を保ったまま focal loss 的な強調ができる。
- 代替案: soft target 全体を 1 つの `pt = sum(s * p)` に潰してサンプル単位で重み付けする。
  - 不採用理由: 候補ごとの難易度差が消え、soft target CE を batch-candidate classification として扱う意図からずれる。

3. `configs/contrastive/model/mxclr.yaml` に `gamma: 0.0` を追加し、main spec には `gamma=0` が現行式、`gamma>0` が focal-style weighting を有効化する契約として同期する。

- 理由: Hydra 解決結果だけで loss 強度を追跡でき、再現性要件を満たせる。

## Risks / Trade-offs

- [Risk] `gamma` を大きくすると easy candidate の寄与が急減し、学習が不安定になる可能性がある。
  Mitigation: 既定値を 0.0 に保ち、設定 override で段階的に sweep できるようにする。
- [Risk] `p` の計算で対角 `-inf` を含むため数値処理を誤ると NaN を生む。
  Mitigation: 既存の off-diagonal mask を再利用し、focal weight も同じ mask 下で集計する。
