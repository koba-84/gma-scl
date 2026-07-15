## Why

MXCLR and MXCLRRank currently use raw cosine similarity for the learned
embedding-side sample-sample distribution. The experiment needs a t-vMF-style
similarity transform controlled by a single concentration parameter while
preserving the current cosine behavior at `kappa=0`.

## What Changes

- Add a `kappa` runtime/config parameter to MXCLR and MXCLRRank.
- Apply the t-vMF transform to learned embedding-side sample-sample cosine
  similarities after cosine computation.
- Keep reference-side graph construction unchanged.
- Do not add a `similarity_type` or other switching config.

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: MXCLR-family learned embedding similarity must support the
  t-vMF transform through `kappa`.

## Impact

- Affected code: `src/models/loss/mxclr.py`,
  `src/models/loss/mxclr_rank.py`, MXCLR-family configs, and focused tests.
- No dependency changes.
