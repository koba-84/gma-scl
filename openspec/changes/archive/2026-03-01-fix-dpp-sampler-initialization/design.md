## Context

DPP埋め込み設定は `on_train_epoch_start` で行っているが、Lightning はその前に train dataloader iterator を構築するため、`DPPBatchSampler.__iter__` が先に呼ばれて未初期化例外が発生する。表示上は最後に `combined_loader` エラーが出るが、一次原因は sampler 未初期化である。

## Goals / Non-Goals

**Goals:**

- DPP利用時に最初のiter開始前に sampler 初期化を完了させる。
- 既存の epoch ごとの埋め込み更新挙動を維持する。
- GCBS/通常shuffleへの影響を最小化する。

**Non-Goals:**

- DPPアルゴリズムやサンプリング分布の変更
- 学習ループ全体の構造変更

## Decisions

- Decision 1: sampler 更新処理を共通メソッド化し、`on_fit_start` と `on_train_epoch_start` から呼ぶ。

  - Rationale: fit開始時に一度だけ確実に初期化しつつ、epoch更新を継続できる。
  - Alternative: DPPBatchSamplerの未初期化時に逐次サンプリングへフォールバックする。
  - Why not: DPP有効化の意図と異なるバッチ生成になり、実験条件が不明瞭になる。

- Decision 2: `DPPBatchSampler.is_initialized()` を追加して二重初期化を避ける。

  - Rationale: `on_fit_start` 後に `on_train_epoch_start` が走るため、不要な再計算を防ぐ。

## Risks / Trade-offs

- [Risk] fit開始時に埋め込み計算が追加され初回待ち時間が増える → Mitigation: 既存のepoch開始計算と同等処理であり、総計算量の増加は限定的。
- [Risk] 更新処理の共通化で条件分岐ミスが入る → Mitigation: DPP/GCBS判定を一箇所に集約し、最小実行でDPP起動確認を行う。
