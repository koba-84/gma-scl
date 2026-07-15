## Context

MXCLR は Hydra config group で agg family ごとの差分を切り替えていますが、現状の agg YAML は `agg`, `graph_builder.agg`, `graph_builder.strategy` を重複して保持しています。実際には family 判定は `agg` だけで足り、`graph_builder` 側に必要なのは center / idf / npmi のような追加フラグだけです。

## Decisions

### Decision 1: agg を唯一の selector にする

- `MXCLR.score_graph()` は `self.agg` を `graph_builder` に明示的に渡す
- `_build_mxclr_graph` は受け取った `agg` から similarity family / transport family を判定する
- transport path の strategy も `agg` をそのまま使う

### Decision 2: graph_builder config は差分フラグだけ持つ

- `configs/contrastive/model/mxclr.yaml` に共通の `graph_builder` target を置く
- agg group は `agg` と optional な `graph_builder` override だけを持つ
- `graph_builder.agg` と `graph_builder.strategy` は全廃する

### Decision 3: transport mass choice も agg から解決する

- `wmd` は frequency mass、`wrd` と `uot` は embedding norm mass を使う
- `weight_source` は config ではなく code 側の family policy として扱う
- unsupported agg は既存どおり MXCLR 初期化で失敗させる

## Consequences

- agg config の重複が減り、Hydra resolve 出力が短くなる
- graph builder partial config は「追加フラグの束」として読みやすくなる
- MXCLR と pytest の helper も agg を唯一の selector とする構造に揃う
