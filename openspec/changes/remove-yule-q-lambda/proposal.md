## Why

`yule_q_lambda` is no longer part of the MXCLR experiment surface, but it is still exposed in configs, aggregator constructors, and target-similarity plumbing. Keeping the unused beta path increases reproducibility review cost and leaves a second association statistic mixed into NPMI-aware aggregations.

## What Changes

- **BREAKING** Remove `yule_q_lambda` from all MXCLR aggregation configs and constructors.
- Remove runtime Yule's Q statistic requests from MXCLR aggregation routing.
- Remove Yule's Q blending from NPMI-aware target graph construction.
- Keep non-runtime label statistic utilities only if they remain independently tested and used outside the removed config path.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `training`: NPMI-aware MXCLR agg configs no longer expose the removed `yule_q_lambda` argument.
- `mxclr-target-association-similarity`: MXCLR target association similarity no longer supports a Yule's Q beta term.

## Impact

- Affects MXCLR aggregation modules, Hydra agg configs, config tests, and MXCLR loss tests.
- Existing configs or scripts that pass `yule_q_lambda` will fail instead of being accepted through a compatibility layer.
- No dependency changes are expected.
