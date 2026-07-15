## MODIFIED Requirements

### Requirement: Distill MXCLR agg exposes centering and KoLeo hyperparameters

MXCLR の `distill_chamfer` と `distill_idf_chamfer` config は、Sentence-BERT 埋め込みの変換方法と正則化強度を Python 実装へ明示的に渡さなければならない。

#### Scenario: Resolve distill_chamfer with sinkhorn centering defaults

- **WHEN** 開発者が `PROJECT_ROOT=$(pwd) uv run python src/train.py --cfg job --resolve contrastive/model=mxclr contrastive/model/agg@contrastive.model.loss_fn=distill_chamfer` を実行する
- **THEN** `contrastive.model.loss_fn.agg.centering` は `sinkhorn_knopp` として解決される
- **AND** `contrastive.model.loss_fn.agg.sinkhorn_knopp_n_iters` は `3` として解決される
- **AND** `contrastive.model.loss_fn.agg.lambda_koleo` は `0.1` として解決される

#### Scenario: Resolve distill_idf_chamfer with sinkhorn centering defaults

- **WHEN** 開発者が `PROJECT_ROOT=$(pwd) uv run python src/train.py --cfg job --resolve contrastive/model=mxclr contrastive/model/agg@contrastive.model.loss_fn=distill_idf_chamfer` を実行する
- **THEN** `contrastive.model.loss_fn.agg.centering` は `sinkhorn_knopp` として解決される
- **AND** `contrastive.model.loss_fn.agg.sinkhorn_knopp_n_iters` は `3` として解決される
- **AND** `contrastive.model.loss_fn.agg.lambda_koleo` は `0.1` として解決される

### Requirement: Distill MXCLR agg supports mean and sinkhorn_knopp centering

distill 系 agg は平均引き centering と Sinkhorn-Knopp centering の両方を受け付け、どちらでも有限な [0, 1] score graph を返さなければならない。

#### Scenario: Distill score graph remains finite under sinkhorn centering

- **WHEN** `DistillChamferGraph` または `DistillIdfChamferGraph` が `centering=sinkhorn_knopp` で label embedding から score graph を構築する
- **THEN** 出力 graph は有限で対称であり
- **AND** 値域は `[0, 1]` に収まる

### Requirement: MXCLR applies KoLeo regularizer only on label-driven distill paths

MXCLR は label 行列から distill 系 score graph を構築する経路に限って KoLeo regularizer を加算し、graph 直入力経路には追加しない。

#### Scenario: MXCLR adds KoLeo term on labels input

- **WHEN** `MXCLR.forward(z, labels)` が distill 系 agg で呼ばれる
- **THEN** contrastive 本体 loss に `lambda_koleo * koleo(label_embeddings)` が加算される
- **AND** KoLeo 入力は事前に L2 normalize される

#### Scenario: MXCLR skips KoLeo term on direct graph input

- **WHEN** `MXCLR.forward(z, g_soft)` が `[N, N]` の direct graph 入力で呼ばれる
- **THEN** `MXCLR` は score graph 再計算を行わず
- **AND** KoLeo regularizer も追加しない
