## ADDED Requirements

### Requirement: MXCLR config must expose aggregation mode

The training configuration MUST allow selecting MXCLR label aggregation by passing agg to loss_fn initialization.

#### Scenario: Resolve MXCLR config with agg option

- **WHEN** 開発者が `contrastive/model=mxclr` を解決する
- **THEN** `loss_fn` は `agg` 設定値を受け取り `src.models.loss.mxclr.MXCLR` に渡せる

#### Scenario: Training fails fast on invalid MXCLR agg

- **WHEN** 開発者が未対応の `loss_fn.agg` を指定して学習を開始する
- **THEN** MXCLR 初期化時に ValueError が送出される
