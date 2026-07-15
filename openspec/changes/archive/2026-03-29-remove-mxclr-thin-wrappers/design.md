## Context

MXCLR の score graph pipeline は前回の統一で family 差分を `_build_mxclr_graph` に集約しましたが、`_build_graph` と `_distance_to_score` が薄い wrapper として残りました。どちらも 1 箇所からしか使われず、役割名も追加情報を持たないため、可読性より探索コストを増やしています。

## Decisions

### Decision 1: `_distance_to_score` は `_build_mxclr_graph` に戻す

- transport distance を `[0, 1]` score に写像する式は transport branch の最終段に直接置く
- score 化式を別 helper に切り出さない

### Decision 2: `_build_graph` は `score_graph` に戻す

- builder registry の解決は唯一の call site である `score_graph` に直接記述する
- top-level helper は複数 call site を持つものだけ残す

## Consequences

- MXCLR top-level helper は matrix 構築や transport weight のような意味を持つ処理だけが残る
- score graph の呼び出し経路は `score_graph -> instantiate(builder) -> _build_mxclr_graph` まで短縮される
