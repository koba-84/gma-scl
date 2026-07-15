## Context

tokenized training input 契約へ移行後も、contrastive sampler refresh は `get_train_texts()` で raw text を再取得し、Encoder 内で再トークナイズしている。これにより epoch ごとに不要な CPU 前処理が残る。

## Goals / Non-Goals

**Goals:**
- GCBS/DPP refresh 経路を tokenized tensor 入力へ統一する。
- refresh 経路で raw text 依存を排除する。
- 既存 sampler ロジック（GCBS permutation / DPP embedding set）は維持する。

**Non-Goals:**
- GCBS/DPP のアルゴリズム変更
- loss / optimizer / scheduler の変更

## Decisions

- Decision 1: ContrastiveDataModule に tokenized refresh batch iterator を追加する。
  Rationale: モジュール側が DataLoader 風に連続バッチを取得でき、既存 refresh ループに統合しやすい。

- Decision 2: ContrastiveLitModule の `_compute_gcbs_embeddings` は tokenized batch list を受ける。
  Rationale: refresh 内で tokenizer を呼ばないことを保証できる。

- Decision 3: refresh 用 batch size は `batch_size_per_device` を流用する。
  Rationale: 既存設定との整合を保ち、新しい設定キーを増やさない。

## Risks / Trade-offs

- [Risk] refresh 時の GPU メモリ使用量が増える可能性 → Mitigation: 現行 batch_size を流用し、OOM 時は既存 batch 設定で調整可能。
- [Risk] sampler refresh の回帰 → Mitigation: integration test で GCBS/DPP path を維持確認する。
