## Context

前回変更で MXCLR に semantic 類似度初期化を追加したが、`use_label_semantic_similarity` が false の場合に fallback が残っている。ユーザー要件は常時 semantic 利用であり、分岐を削除して初期化契約を単純化する必要がある。

## Goals / Non-Goals

**Goals:**

- semantic 有効/無効フラグを廃止する。
- MXCLR が常にラベル説明から類似度行列を構築する状態にする。
- 設定と仕様の記述を実装契約に一致させる。

**Non-Goals:**

- Sentence-BERT モデルの変更。
- AAPD 以外データセット対応。

## Decisions

- Decision 1: `use_label_semantic_similarity` を `__init__` 引数から削除する。
- Decision 2: `label_description_path` を必須引数化し、未指定時は初期化で `ValueError` を送出する。
- Decision 3: `similarity_graph` から fallback 分岐を削除し、semantic 行列ベース計算のみを残す。

## Risks / Trade-offs

- [Risk] 設定ミス時に初期化が失敗しやすくなる。
  - Mitigation: 例外メッセージを明確化する。
- [Risk] 旧設定ファイルとの互換がなくなる。
  - Mitigation: BREAKING として specs に明記する。
