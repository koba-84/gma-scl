## ADDED Requirements

### Requirement: Contrastive embedding normalization ownership

Contrastive 学習で loss に入力する埋め込み正規化は `src/models/contrastive_module.py` の `ContrastiveLitModule._project` が MUST 担当し、loss 実装側は同等の正規化を重複実装してはならない。

#### Scenario: Projection path before loss call

- **WHEN** `ContrastiveLitModule.model_step` が batch を処理する
- **THEN** `ContrastiveLitModule._project` が `projection_head` 出力に L2 正規化を適用した埋め込みを生成し、その値が loss に渡される

#### Scenario: MXCLR forward behavior

- **WHEN** 開発者が `src/models/loss/mxclr.py` の `MXCLR.forward` 実装を確認する
- **THEN** `MXCLR.forward` に埋め込み正規化処理が存在しない

#### Scenario: Resolve MXCLR from Hydra config

- **WHEN** 開発者が `configs/contrastive/model/mxclr.yaml` の `loss_fn._target_` を使ってインスタンス化する
- **THEN** `src.models.loss.mxclr.MXCLR` が解決される
