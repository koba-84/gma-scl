## Context

MXCLR は初期化時に `label_description_path` を読み込み、Sentence-BERT でラベル埋め込みを構築する。現行 config は `data/aapd/arxiv_label_descriptions.json` を指すが、リポジトリに存在する JSON は `data/aapd/label_descriptions.json` であるため、train entrypoint からの instantiate が FileNotFoundError になる。

## Goals / Non-Goals

**Goals:**

- 既定の `contrastive/model=mxclr` が実在ファイルを参照する
- config 解決だけでなく model instantiate でも失敗しないことを test で固定する

**Non-Goals:**

- MXCLR の埋め込み計算ロジック変更
- データ生成スクリプトの出力仕様変更

## Decisions

- Decision 1: config 側の参照先を `data/aapd/label_descriptions.json` に修正する
  - Rationale: 既存データ資産と最小差分で整合する
  - Alternative considered: 実装側で存在しない旧ファイル名から新ファイル名へ fallback する
  - Rejected because: 後方互換レイヤー追加になり、研究用 repo の方針に反する
- Decision 2: test は `contrastive/model=mxclr` を compose し、SBERT encode を monkeypatch して instantiate 可否だけを見る
  - Rationale: 既定 config の path 契約を直接検証できる

## Risks / Trade-offs

- [Risk] docs/spec のファイル名が残ると再発する → Mitigation: main spec の参照名も同時に更新する
