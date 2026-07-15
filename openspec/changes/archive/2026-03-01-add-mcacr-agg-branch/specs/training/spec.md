## ADDED Requirements

### Requirement: MCACR config must expose aggregation mode

The training configuration MUST allow selecting MCACR repulsion aggregation by passing agg to loss_fn initialization.

#### Scenario: Resolve MCACR config with agg option

- **WHEN** 開発者が `contrastive/model=mcacr` を解決する
- **THEN** `loss_fn` は `agg` 設定値を受け取り `src.models.loss.mcacr.MCACRLoss` に渡せる

#### Scenario: Training fails fast on invalid MCACR agg

- **WHEN** 開発者が未対応の `loss_fn.agg` を指定して学習を開始する
- **THEN** MCACR 初期化時に ValueError が送出される
