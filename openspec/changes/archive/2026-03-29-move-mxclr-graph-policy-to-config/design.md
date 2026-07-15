## Context

MXCLR は現在 `graph_builder` に共通 builder 関数を置き、`agg` から similarity / transport とその policy を分岐しています。これは loss 側の instantiate ベース構成と揃っておらず、agg だけが selector 文字列と共通 dispatcher を必要としています。

## Decisions

### Decision 1: agg config group が concrete 実装を直接選ぶ

- `configs/contrastive/model/agg/*.yaml` は concrete graph 実装の `_target_` を持つ
- `configs/contrastive/model/mxclr.yaml` の共通 `graph_builder` target は削除する
- agg group override は concrete 実装の差し替えとして働く

### Decision 2: MXCLR 本体は selector を解釈しない

- `MXCLR.score_graph()` は注入された `graph_builder` を呼ぶだけにする
- `agg` は設定可読性のために保持してよいが、実行分岐に使わない
- `_build_mxclr_graph` と agg 逆引き helper は削除する

### Decision 3: concrete 実装は class として定義する

- agg ごとの graph 実装は concrete class にする
- class の公開 API は同じ call シグネチャを共有する
- 共通計算は private helper に留め、public な総称 builder は置かない

## Consequences

- agg 側も loss と同じく instantiate で実装選択する形に揃う
- MXCLR 本体は graph 実装の dispatcher を持たなくなる
- resolve 結果では `graph_builder._target_` が agg ごとに変わり、selector 用補助キーは不要になる
