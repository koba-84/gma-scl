## Why

Prediction analysis currently reports metrics from one saved artifact per model, which hides seed variance and makes multi-seed experiment summaries manual. The scripts should consume seed-specific prediction artifacts such as `bce0.pt` and report model-level averages reproducibly.

## What Changes

- Update AAPD, Reuters-21578, and UKLEX prediction analysis scripts to discover seed-suffixed artifact files for each model.
- Compute Macro-F1 for each seed artifact independently, then report both the per-seed values and the mean per model and metric column.
- Require at least one seed artifact per configured model and fail with a clear error when none are found.
- **BREAKING**: The analysis scripts no longer read unsuffixed files such as `bce.pt`; inputs must be named with an integer seed suffix such as `bce0.pt`.

## Capabilities

### New Capabilities

### Modified Capabilities

- `prediction-analysis`: prediction artifact lookup and reported values change from single-artifact metrics to seed-suffixed multi-seed averages.

## Impact

- Affected scripts: `scripts/a.py`, `scripts/b.py`, `scripts/c.py`.
- Affected specs: `openspec/specs/prediction-analysis/spec.md`.
- No dependency changes.
