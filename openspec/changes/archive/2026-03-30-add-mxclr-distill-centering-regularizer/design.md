## Context

distill 系 agg はラベル埋め込み同士の類似度行列を先に構築し、その後に chamfer 集約で sample-pair score graph を作っています。今回の変更は、この前段のラベル埋め込み変換と、MXCLR loss への補助正則化の 2 箇所に限定されます。

参照元として、DINOv2 は teacher 出力に対して `sinkhorn_knopp_teacher(..., n_iterations=3)` を用意し、KoLeo regularizer では L2 正規化後の最近傍距離に `-log(distance)` を適用しています。

## Decisions

### Decision 1: distill 系 agg に centering strategy を持たせる

- `DistillChamferGraph` と `DistillIdfChamferGraph` に `centering` と `sinkhorn_knopp_n_iters` を持たせる
- `centering=mean` のときは現行どおり feature-wise mean subtraction を使う
- `centering=sinkhorn_knopp` のときはラベル埋め込みを温度 1.0 の logits とみなし、列和 1・行和 `1 / num_labels` に近づける Sinkhorn-Knopp 反復を 3 回適用する
- centering 後も類似度行列構築前に有限値・正ノルム検証を維持する

### Decision 2: KoLeo regularizer は agg module が公開し、MXCLR forward で加算する

- distill 系 agg module に `regularizer(label_embeddings)` を追加する
- regularizer 内部では DINOv2 に合わせて入力を L2 normalize し、自己対角を除いた最大内積相手との L2 距離から `-log(distance + eps)` を取る
- `lambda_koleo=0.1` は agg config に置き、`MXCLR.forward(z, labels)` 時のみ contrastive loss へ加算する
- `MXCLR.forward(z, g_soft)` の direct graph 経路では regularizer を加えない

### Decision 3: Hydra config と spec は distill 系専用 hyperparameter を明示する

- `configs/contrastive/model/agg/distill_chamfer.yaml` と `distill_idf_chamfer.yaml` に `centering: sinkhorn_knopp`、`sinkhorn_knopp_n_iters: 3`、`lambda_koleo: 0.1` を追加する
- main training spec に、distill 系 agg config が centering strategy と KoLeo weight を持つことを追記する

## Consequences

- distill 系 agg だけが DINOv2 由来の assignment centering と feature spreading regularization を持ち、他 agg family の契約は変えない
- `score_graph(labels)` は従来どおり [0, 1] の対称行列を返し続ける
- `forward(z, labels)` と `forward(z, g_soft)` の値は一致しなくなる可能性があるが、これは regularizer が labels 経路でのみ定義されるためであり、契約として明示する
