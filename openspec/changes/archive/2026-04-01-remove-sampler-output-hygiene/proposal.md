## Why

sampler runtime の stdout cleanliness は、研究リポジトリとして重視すべき再現性・データ契約・学習挙動の system-level contract ではない。現在の `sampler output hygiene` requirement と targeted pytest は実装都合の hygiene を main spec に持ち込みすぎており、保守対象を不必要に広げている。

## What Changes

- training spec から sampler output hygiene requirement と dedicated targeted test policy を削除する。
- `tests/test_sampler_output_hygiene.py` を削除する。
- `src/data/components/dpp.py` の third-party stdout 抑止実装を削除し、DPP sampler の functional contract のみに責務を絞る。

## Capabilities

### New Capabilities

- None

### Modified Capabilities

- `training`: sampler の system-level contract から runtime output hygiene を除外する

## Impact

- `openspec/specs/training/spec.md`
- `openspec/specs/training.md`
- `tests/test_sampler_output_hygiene.py`
- `src/data/components/dpp.py`
