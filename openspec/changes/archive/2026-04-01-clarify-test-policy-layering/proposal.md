## Why

sampler 固有 test と parametrized integration test の境界が spec 上で明文化されておらず、DPP 固有の stdout 回帰 test の意図が読み取りにくい。あわせて、この repo が test でどの層をどこまで確認するのかが training spec と pytest 規約に分散しており、保守時の判断基準が不透明になっている。

## What Changes

- pytest 側の test policy に「どの層で何を確認するか」と「いつ parametrization を使い、いつ個別 test を残すか」の基準を追加する。
- training 側の sampler policy に、sampler 共通 integration test と sampler 固有 compatibility test の責務分離を追加する。
- DPP の stdout hygiene は sampler 一般 contract ではなく、DPP 実装が third-party dependency と接続する際の個別 compatibility contract として位置づける。

## Capabilities

### New Capabilities

- None

### Modified Capabilities

- `dev-quality-tooling`: pytest の test 層ポリシーと parametrization の適用基準を明文化する
- `training`: sampler integration test と sampler 固有 compatibility test の責務境界を明文化する

## Impact

- `openspec/specs/dev-quality-tooling/spec.md`
- `openspec/specs/training/spec.md`
- `openspec/specs/training.md`
- `tests/test_dpp_sampler_stdout.py` と `tests/test_data_integration.py` の読み方に関する project policy
