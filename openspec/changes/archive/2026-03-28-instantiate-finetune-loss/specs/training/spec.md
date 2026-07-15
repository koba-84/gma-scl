## MODIFIED Requirements

### Requirement: Classification finetune loss must resolve through instantiate config

Classification finetune stage MUST resolve its loss function through a Hydra-instantiated `criterion` config object. The finetune module MUST NOT select loss implementations through internal `loss_name` string branching.

#### Scenario: Instantiate finetune criterion from composed config

- **WHEN** 開発者または coding agent が classification stage config を compose して `cfg.classification.model` を instantiate する
- **THEN** `criterion` は `_target_` を持つ loss config から生成される
- **AND** `FinetuneLitModule` は `loss_name` や `loss_kwargs` の文字列分岐を持たない

#### Scenario: Swap classification loss variants by config only

- **WHEN** 開発者または coding agent が BCE、Asymmetric、ZLPR のいずれかへ loss variant を切り替える
- **THEN** 切り替えは `configs/classification/loss/*.yaml` の compose または override だけで完了する
- **AND** module 実装の追加分岐変更を必要としない
