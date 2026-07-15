## ADDED Requirements

### Requirement: Contrastive epoch sweep configuration

The training configuration SHALL provide a dedicated hparams_search preset for sweeping contrastive training epochs over 1, 5, 10, and 20.

#### Scenario: Run epoch sweep via Hydra multirun

- **WHEN** a developer runs `uv run python src/train.py -m hparams_search=contrastive_epoch`
- **THEN** Hydra sweeps `contrastive.trainer.max_epochs` across `1,5,10,20`
- **AND** each run executes with base contrastive model and the default classification stage (train/test enabled)

## MODIFIED Requirements

### Requirement: train.yaml defaults include both stages

This requirement SHALL keep both training stages in configs/train.yaml defaults.
configs/train.yaml の defaults は以下（確定）：

- `contrastive: train`
- `classification: train`
- `hydra: default`

→ デフォルトでは contrastive と classification の設定を読み込む。
また、`configs/contrastive/train.yaml` の defaults では contrastive model として `base` を既定値にしなければならない。

#### Scenario: Default stage configs are loaded

- **WHEN** 開発者が `uv run python src/train.py --cfg job --resolve` を実行する
- **THEN** train 設定は contrastive と classification の両ステージを読み込む
- **AND** contrastive model は `base` が解決される
