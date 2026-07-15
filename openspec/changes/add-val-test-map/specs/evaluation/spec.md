## MODIFIED Requirements

### Requirement: Evaluation target stage

Evaluation flow MUST execute test for the classification stage in default configuration and MUST expose the standard classification test metrics including multilabel mAP.

#### Scenario: Run default evaluation path

- **WHEN** 開発者が既定設定で train/eval 経路を実行する
- **THEN** classification stage の test が実行される
- **AND** 出力 metric には `classification/test/f1_micro` と `classification/test/map` が含まれる
