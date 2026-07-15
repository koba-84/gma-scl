## Why

MXCLR-family target graphs currently blend label-description cosine similarity with NPMI, but co-occurrence association can be better captured by a contingency-table statistic that remains defined for sparse label pairs. Adding Yule's Q with Haldane-Anscombe 0.5 correction makes this target-similarity component explicit and reproducible for comparison experiments.

## What Changes

- Add train.csv-derived pairwise Yule's Q computation with Haldane-Anscombe 0.5 correction.
- Add an explicit MXCLR aggregation hyperparameter for the Yule's Q contribution.
- Extend NPMI-blended MXCLR agg modules to compute target label similarity as alpha cosine plus one minus alpha times the NPMI/Yule mixture, where alpha is the existing cosine-vs-statistic mixing weight.
- Update configs, tests, and main specs so the new hyperparameter is visible in reproducibility review.

## Capabilities

### New Capabilities

- `mxclr-target-association-similarity`: Defines MXCLR target label similarity blending with NPMI and corrected Yule's Q.

### Modified Capabilities

- `training`: Supported MXCLR-family configs and loss aggregation contracts expose the new Yule's Q hyperparameter.

## Impact

- Affected code: `src/models/loss/components/label_stats.py`, MXCLR agg modules under `src/models/loss/agg/`, and MXCLR-family configs.
- Affected tests: targeted loss/statistics tests and config resolution tests.
- No new runtime dependency is required.
