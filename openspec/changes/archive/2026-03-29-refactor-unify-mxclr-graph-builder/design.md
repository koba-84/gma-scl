## Context

MXCLR は loss 本体では sample-pair の soft target score 行列しか消費しない一方で、実装上は similarity family と transport family の graph builder が別関数として並んでいました。さらに `_build_graph` と `MXCLR_GRAPH_BUILDERS` は存在しても、`MXCLR` クラス本体はその経路を使っておらず、責務の境界が分断されていました。

## Decisions

### Decision 1: graph builder の公開契約は score graph に統一する

- builder の返り値は一貫して MXCLR が直接 soft target として使う `[N, N]` score 行列にする
- similarity family は共通 aggregation helper の出力をそのまま score として返す
- transport family は pairwise transport helper が返す距離を `[0, 1]` の score に写像して返す

### Decision 2: family ごとの差分は instantiate 設定へ押し込む

- top-level の公開 builder 関数は `_build_mxclr_graph` 1 本にする
- `MXCLR_GRAPH_BUILDERS` は `matrix_kind`, `strategy`, `weight_source`, `blend_npmi`, `use_label_idf`, `center_embeddings` などの差分だけを持つ
- matrix 構築や mass 選択の差分は private helper に残し、family 別の top-level builder は作らない

### Decision 3: MXCLR クラス本体も同じ graph pipeline を使う

- `MXCLR` は label description から semantic similarity ではなく label embeddings を保持する
- labels から graph を作る公開 API は `score_graph(labels)` とし、`forward` も同じ API を使う
- transport / distill 系の graph 構築に必要な label-side tensor は optional 引数で受け、未指定時は該当 agg で明示的に失敗させる

## Consequences

- `similarity_graph` という名前は廃止され、公開 API は score 契約に寄る
- transport 系 helper の未接続状態が解消され、MXCLR 本体からも同じ builder registry を経由する
- score graph 契約が明示されるので、pytest では similarity 系と transport 系を同じ観点で検証できる
