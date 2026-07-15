## MODIFIED Requirements

### Requirement: Loss-unit checks stay outside evaluation flow

評価仕様は統合経路を対象とし、loss 単体検証の標準入口は pytest として分離されなければならない。

#### Scenario: Keep evaluation focused on integration

- **WHEN** 開発者または coding agent が evaluation 関連の検証手順を参照する
- **THEN** loss 単体検証は pytest で扱うと明記される
- **AND** evaluation flow の標準検証は `tests/eval.py` を中心とした統合テストとして扱われる
