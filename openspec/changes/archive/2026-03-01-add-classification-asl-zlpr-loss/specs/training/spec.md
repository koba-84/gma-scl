## ADDED Requirements

### Requirement: Classification loss function selection

classification stage model MUST resolve loss function from configuration and support `bce`, `asymmetric`, and `zlpr`.

#### Scenario: Select asymmetric loss in classification config

- **WHEN** 開発者が classification model config で `loss_name=asymmetric` を指定する
- **THEN** 学習時の criterion は Asymmetric Loss として初期化される

#### Scenario: Select zlpr loss in classification config

- **WHEN** 開発者が classification model config で `loss_name=zlpr` を指定する
- **THEN** 学習時の criterion は ZLPR loss として初期化される

### Requirement: Asymmetric loss hyperparameter contract

Asymmetric loss implementation MUST accept `gamma_pos`, `gamma_neg`, and `margin` hyperparameters from configuration.

#### Scenario: Use requested ASL hyperparameters

- **WHEN** 開発者が `gamma_pos=0`, `gamma_neg=1`, `margin=0` を設定する
- **THEN** Asymmetric loss はその値で forward 計算を行う

## MODIFIED Requirements

### Requirement: Stage defaults in train config

The train configuration SHALL include both contrastive and classification stages by default.

#### Scenario: Resolve default train config

- **WHEN** 開発者が `uv run python src/train.py --cfg job --resolve` を実行する
- **THEN** 設定に contrastive と classification の両方が含まれる
- **AND** classification.model の損失設定を解決してインスタンス化できる
