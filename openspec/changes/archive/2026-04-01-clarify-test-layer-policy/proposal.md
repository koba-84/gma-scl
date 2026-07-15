# Proposal: clarify-test-layer-policy

## Why

旧 `tests/test_dpp_sampler_stdout.py` は DPP 固有の stdout 抑止を検証していたが、現状では「sampler 全体の output hygiene policy」との関係が読み取りにくい。あわせて、repo 全体の pytest がどの層で何を確認するかの方針が `training` と `dev-quality-tooling` に分散しており、`parametrize` でまとめるべき境界も判断しづらい。

## What Changes

- sampler 実行時の output hygiene を repo-owned sampler runtime の共通方針として明文化する。
- pytest の責務分担を、property / targeted contract / integration / slow・gpu の層として仕様化する。
- `parametrize` は「同一 assertion contract の独立ケース」に限定し、異なる契約を 1 test body に混在させない方針を仕様へ追加する。
- DPP 専用 stdout test を GCBS/DPP を含む sampler output hygiene test に置き換える。

## Impact

- 影響仕様: `openspec/specs/training/spec.md`, `openspec/specs/dev-quality-tooling/spec.md`
- 影響コード: `tests/test_sampler_output_hygiene.py`
- 検証: targeted pytest, `uv run pre-commit run -a`, OpenSpec validate
