## ADDED Requirements

### Requirement: Idf chamfer config exposes transport lambda

The `idf_chamfer` MXCLR agg config MUST define `transport_lambda` so that Hydra can override it without using additive `+` syntax.

#### Scenario: Override idf chamfer transport lambda

- **WHEN** 開発者が `uv run python src/train.py --cfg job --resolve contrastive/model=mxclr contrastive/model/agg@contrastive.model.loss_fn=idf_chamfer contrastive.model.loss_fn.agg.transport_lambda=5e-1` を実行する
- **THEN** 設定解決は struct error を出さずに成功する
- **AND** `contrastive.model.loss_fn.agg.transport_lambda` は `5e-1` として解決される
