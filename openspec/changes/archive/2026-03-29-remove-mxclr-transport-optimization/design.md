## Context

MXCLR の transport family は WMD、WRD、UOT いずれも Python Optimal Transport の sinkhorn 系 solver を使うように整理済みです。`transport_optimization` は balanced path で `"sinkhorn"` 以外を拒否するだけで、実際の選択肢を提供していません。

## Decisions

### Decision 1: MXCLR から transport backend 選択引数を削除する

- `MXCLR.__init__` から `transport_optimization` を削除する
- `_build_mxclr_graph` からも同名引数を削除し、transport family は内部でそのまま `pairwise_transport` を呼ぶ
- score graph 構築時に transport backend の分岐は持たない

### Decision 2: pairwise_transport の公開契約も sinkhorn 固定へ寄せる

- `pairwise_transport` から `optimization` 引数を削除する
- balanced family は `_pairwise_balanced_distance`、unbalanced family は既存の unbalanced sinkhorn 実装をそのまま使う
- unsupported optimization の validation は不要になる

### Decision 3: agg config と spec は backend 固定を前提にする

- transport 系 agg config は `transport_optimization` を持たない
- training spec は MXCLR agg config の必須解決値から `transport_optimization` を外す
- transport helper contract も strategy selector のみを公開入力として扱う

## Consequences

- MXCLR transport family の設定面が短くなり、切り替え可能であるかのような誤解を避けられる
- graph builder と transport helper の署名が短くなり、不要な validation も消える
- sinkhorn 固定という現在の実装方針が spec と一致する
