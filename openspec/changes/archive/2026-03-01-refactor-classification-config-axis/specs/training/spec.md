## ADDED Requirements

### Requirement: Classification config shall use strategy and loss axes

classification stage configuration MUST provide independent Hydra config groups for strategy and loss selection.

#### Scenario: Resolve classification strategy and loss

- **WHEN** 開発者が `classification/strategy=linear_probe` と `classification/loss=asymmetric` を指定して設定を解決する
- **THEN** classification.model は encoder freeze 戦略と asymmetric loss 設定を同時に解決できる

#### Scenario: Resolve finetune with zlpr

- **WHEN** 開発者が `classification/strategy=finetune` と `classification/loss=zlpr` を指定して設定を解決する
- **THEN** classification.model は encoder 非 freeze 戦略と zlpr loss 設定を同時に解決できる

## REMOVED Requirements

### Requirement: Classification model shall be selected by single model config group

**Reason**: 学習戦略と loss の責務分離のため単軸指定を廃止する。
**Migration**: `classification/model=<name>` を `classification/strategy=<name>` と `classification/loss=<name>` に置き換える。

## MODIFIED Requirements

### Requirement: Stage defaults in train config

The train configuration SHALL include both contrastive and classification stages by default.

#### Scenario: Resolve default train config

- **WHEN** 開発者が `uv run python src/train.py --cfg job --resolve` を実行する
- **THEN** 設定に contrastive と classification の両方が含まれる
- **AND** classification.model の損失設定を解決してインスタンス化できる
- **AND** classification.model は strategy と loss の 2 軸設定を defaults で解決できる
