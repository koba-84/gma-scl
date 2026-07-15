## Context

MXCLR は `sbert_model_name` と `label_description_path` を受け取り、`SentenceTransformer.encode()` でラベル説明文を埋め込み化する。現実装では最大トークン長が設定に露出しておらず、モデル既定値へ暗黙依存するため、実験設定の追跡が難しい。

## Goals / Non-Goals

**Goals:**

- MXCLR 設定でラベル説明文エンコードの最大トークン長を明示指定できる。
- 指定値は `SentenceTransformer.max_seq_length` に確実に反映される。
- 既存の学習経路（`contrastive/model=mxclr`）で設定解決できる。

**Non-Goals:**

- ラベル説明文の要約・分割など前処理方針の変更。
- SBERT モデル種別の変更。
- contrastive data 側 tokenization 設定の変更。

## Decisions

1. MXCLR の初期化引数に `sbert_max_length: int` を追加し、既定値を 256 とする。

- 理由: 現行運用モデル `all-MiniLM-L6-v2` の既定長に合わせつつ、Hydra 側で明示上書き可能にする。
- 代替案: `None` 許容で未指定時は既定値利用。
  - 不採用理由: 「明示指定」の要件を満たしにくい。

2. `_encode_descriptions_with_sbert` に `max_length` 引数を追加し、`model.max_seq_length = max_length` を設定してから encode する。

- 理由: トークナイズ上限が実行時に必ず固定され、モデル既定値への暗黙依存を除去できる。

3. `configs/contrastive/model/mxclr.yaml` に `sbert_max_length: 256` を追加する。

- 理由: 設定ファイルだけで上限値を確認できるようにする。

## Risks / Trade-offs

- [Risk] 将来別 SBERT モデルへ切替時に 256 が短すぎる可能性。
  Mitigation: Hydra override で `contrastive.model.loss_fn.sbert_max_length=<値>` を変更可能にする。
- [Risk] max_length 不正値（0以下）で初期化失敗する。
  Mitigation: 初期化時に値検証を行い早期例外化する。
