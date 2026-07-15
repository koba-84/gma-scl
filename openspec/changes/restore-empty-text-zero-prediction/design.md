## Context

旧実装では test_step が text 値を見て `"nan"` 行の予測を 0 化していたが、text payload 削除時にこの処理も削除された。現在は tokenized-only 契約のため、text を戻さずに同等挙動を復元する必要がある。

## Goals / Non-Goals

**Goals:**
- 空テキスト行の予測 0 化を classification test に復元する。
- text payload を戻さず tokenized-only 契約を維持する。

**Non-Goals:**
- train/val の予測ロジック変更
- contrastive 側の損失・サンプラ変更

## Decisions

- Decision 1: 前処理で `is_empty_text` 列を生成する。
  Rationale: ランタイムで raw text を参照せず判定できる。

- Decision 2: DataModule collate で `inputs["empty_text_mask"]` を追加する。
  Rationale: 既存 `(inputs, labels)` 契約を維持しつつ必要情報を搬送できる。

- Decision 3: `FinetuneLitModule.test_step` で `empty_text_mask` を見て `preds[mask]=0` を適用する。
  Rationale: 旧仕様の評価挙動を最小差分で復元する。

## Risks / Trade-offs

- [Risk] 空文字判定の定義差異 → Mitigation: `strip()==""` と `lower()=="nan"` を empty と定義し、仕様に固定する。
