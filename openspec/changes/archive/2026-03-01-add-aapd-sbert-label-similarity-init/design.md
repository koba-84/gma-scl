## Context

AAPD にはラベル説明文マッピング（`data/aapd/arxiv_label_descriptions.json`）が存在するが、現行の MXCLR は labels から機械的にサンプル間類似度を作るのみで、ラベル説明文由来の意味情報を利用していない。今回の変更では、MXCLR 初期化時に AAPD ラベル説明文からラベル間意味類似度行列を構築し、forward 計算で利用できる状態にする。

## Goals / Non-Goals

**Goals:**

- `MXCLR.__init__` で AAPD ラベル説明文を読み込み、Sentence-BERT 埋め込みからラベル間類似度行列を一度だけ構築する。
- 学習時は labels からサンプルごとのラベル集合類似度を計算し、上記ラベル間行列を通じて `g_soft` を作れるようにする。
- 説明ファイル欠損やラベル数不一致は初期化時に明示的エラーとして扱う。

**Non-Goals:**

- ラベル説明文の生成スクリプト自体の変更。
- Sentence-BERT のファインチューニング。
- AAPD 以外データセット向けの説明文マッピング整備。

## Decisions

- Decision 1: `MXCLR.__init__` に以下の引数を追加する。

  - `dataset_name: str = ""`
  - `label_description_path: str | None = None`
  - `sbert_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"`
  - `use_label_semantic_similarity: bool = False`
    理由: 既存の loss 呼び出し契約を壊さず、設定で明示的に有効化できるようにするため。

- Decision 2: 意味類似度行列は初期化時に CPU で計算し、`register_buffer` で保持する。
  理由: 毎 step 再計算を避け、DDP を含む学習時に状態同期しやすくするため。

- Decision 3: `similarity_graph(labels)` は `labels @ label_similarity @ labels^T`（正規化あり）に切り替える。
  理由: ラベル間意味類似度をサンプル間へ反映できるため。semantic 機能が無効時は従来の cosine fallback を使う。

- Decision 4: 依存として `sentence-transformers` を追加し、実装は `SentenceTransformer.encode(...)` を利用する。
  理由: Sentence-BERT 利用要件を最短で満たし、実装の可読性を保つため。

## Risks / Trade-offs

- [Risk] 初期化時にモデルロードコストが増え、起動時間が長くなる。

  - Mitigation: `use_label_semantic_similarity=false` を既定にし、必要時のみ有効化する。

- [Risk] 説明文JSONの順序と学習ラベル次元が一致しないと誤った類似度になる。

  - Mitigation: `labels` 配列の index を使って厳密に並べ、shape 不一致時は例外送出する。

- [Risk] sentence-transformers の追加で環境依存差異が増える。

  - Mitigation: `pyproject.toml` に明示依存追加し、自己テストで初期化経路を検証する。
