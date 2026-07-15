## Context

aapd実行でDPPyのexact k-DPPサンプリング内部から `probabilities do not sum to 1` が発生した。一次原因はDPP確率計算の数値不安定性で、データ規模と `float32` 精度、`GS` モードの誤差蓄積が重なっている可能性が高い。

## Goals / Non-Goals

**Goals:**

- DPPサンプリング経路をより安定な数値設定へ変更する。
- 既存のDPP機能を維持しつつaapd実行を通す。

**Non-Goals:**

- DPPアルゴリズム自体の変更
- GCBS/通常shuffle経路の変更

## Decisions

- Decision 1: `set_embeddings()` で `float64` を使用する。
  - Rationale: 確率計算の丸め誤差を抑え、合計1からのズレを減らす。
- Decision 2: datamoduleのDPP既定モードを `GS_bis` に変更する。
  - Rationale: `GS` より数値安定性が高い実装を既定化する。
- Decision 3: `FiniteDPP` 初期化時の不要な標準出力をDPP sampler側で抑止する。
  - Rationale: DPPyの内部実装が `L_gram_factor` 受け取り時に `print` を実行し、学習ログ可読性を損なうため。

## Risks / Trade-offs

- [Risk] 計算コスト増加（float64） → Mitigation: DPP経路のみ適用し、対象範囲を限定する。
- [Risk] モード変更による性能差異 → Mitigation: モード指定overrideは維持し、必要時に `GS` へ戻せる設計を残す。
- [Risk] 標準出力の過剰抑止で本来のエラー診断ログを隠す可能性 → Mitigation: 抑止範囲を `FiniteDPP` 構築時のみに限定し、例外はそのまま伝播する。
