## Context

現状の `train_dataloader` は単一の DataLoader 呼び出しで `batch_size`/`shuffle`/`sampler`/`batch_sampler` を条件付きで切り替えている。`sampler_type=dpp` の場合に `batch_sampler` を有効化しつつ `batch_size=None` や `drop_last` も渡してしまい、PyTorch DataLoader の排他制約に違反して ValueError が発生する。

## Goals / Non-Goals

**Goals:**

- DPP時に PyTorch の排他制約を満たす DataLoader 引数セットへ修正する。
- GCBSおよび通常shuffleの既存挙動を変更しない。
- 修正がハイパーパラメータ探索の `sampler_type=dpp` ケースで有効であることを確認できる状態にする。

**Non-Goals:**

- DPPサンプリングアルゴリズム自体の変更
- GCBSアルゴリズムやモデル側ロジックの変更
- 追加の最適化やリファクタリング

## Decisions

- Decision 1: `train_dataloader` を DPP分岐と非DPP分岐で明示的に分ける。

  - Rationale: `batch_sampler` を使う経路では DataLoader に `batch_size/shuffle/sampler/drop_last` を渡さない必要があり、単一呼び出しでの条件式より分岐実装の方が誤指定を防げる。
  - Alternative considered: 単一呼び出しのまま全引数を `if self.use_dpp()` でさらに細分化する。
  - Why not: 引数の排他ルールが複雑化して再発リスクが高い。

- Decision 2: 非DPP経路は従来通り `batch_size` ベースを維持する。

  - Rationale: 既存実験条件との互換性を保ち、影響範囲を最小化する。

## Risks / Trade-offs

- [Risk] DPP分岐で `drop_last` が DataLoader 側に渡らなくなる → Mitigation: DPPのバッチ末尾制御は `DPPBatchSampler` 側の `drop_last` に一本化されているため仕様整合性は維持される。
- [Risk] 分岐追加で可読性が低下する → Mitigation: 分岐意図を簡潔にコメントし、引数セットを明示化する。
