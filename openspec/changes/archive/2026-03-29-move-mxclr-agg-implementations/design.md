## Context

MXCLR の concrete graph 実装は instantiate ベースになりましたが、実装本体がまだ `src/models/loss/mxclr.py` に同居しています。これでは loss module と agg 実装 module の境界が曖昧で、可読性が落ちます。

## Decisions

### Decision 1: MXCLR agg 実装は `loss/agg` 配下へ移す

- 新しく `src/models/loss/agg/` を追加する
- MXCLR 用の concrete agg class は `src/models/loss/agg/<agg>.py` に 1 ファイルずつ置く
- agg 実装に閉じた処理は各 module 内へ閉じ込め、共通 builder は置かない

### Decision 2: `mxclr.py` は loss 本体だけを持つ

- `MXCLR` class と `_compute_mxclr_loss`、label description / embedding 初期化まわりだけを残す
- agg 実装 class や transport/similarity graph helper は残さない
- `MXCLR` は `graph_builder` ではなく instantiate 済みの `agg` module を直接受け取る
- agg 文字列 selector に依存した Python 側 dispatch は持たない

### Decision 3: config と tests は新しいモジュールを直接参照する

- agg config は `loss_fn.agg._target_` として `src.models.loss.agg.<agg>.*` を指す
- tests も `src.models.loss.agg.<agg>` から concrete class を import する
- backward compatibility 用 re-export は追加しない

### Decision 4: transport solver は POT の torch backend を使う

- `src/models/loss/components/transport.py` は自前 Sinkhorn iteration を持たない
- balanced path は `ot.sinkhorn2`、unbalanced path は `ot.unbalanced.sinkhorn_unbalanced2` を使う
- cost matrix と label mass の構成は repo 側で行い、solver に torch tensor をそのまま渡す

## Consequences

- `mxclr.py` の責務が loss 本体に限定される
- agg 実装の配置が intent に沿ったものになる
- config / tests から見ても、agg 実装が loss 本体と別 module だと明確になる
