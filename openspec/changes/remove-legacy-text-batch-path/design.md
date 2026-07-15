## Context

現在の実装は tokenized pipeline へ移行済みだが、Encoder に raw text 入力分岐、DataModule の texts 同梱、Finetune test の text マスク処理が残っている。これらは互換層であり、本番経路の可読性と保守性を下げる。

## Goals / Non-Goals

**Goals:**
- minibatch 契約を `(inputs, labels)` に固定する。
- Encoder を tokenized tensors 専用にする。
- stage モジュールから raw-text 分岐ロジックを削除する。

**Non-Goals:**
- sampler アルゴリズム変更
- モデル構造・学習ハイパーパラメータ変更

## Decisions

- Decision 1: DataModule collate は texts を返さない。
  Rationale: 学習ステップで未使用データを運搬しない。

- Decision 2: Encoder の tokenizer メンバと text fallback を削除する。
  Rationale: Data preprocessing で tokenization を完了させる設計に統一する。

- Decision 3: Finetune の `nan` text 特例処理を削除する。
  Rationale: text payload を廃止するため、挙動を label/logit ベースに限定する。

## Risks / Trade-offs

- [Risk] text 依存の既存検証コードが壊れる → Mitigation: integration test を batch 契約中心に更新する。
- [Risk] 外部スクリプトが旧入力契約を想定 → Mitigation: spec に BREAKING を明記し、変更を commit message に記録する。
