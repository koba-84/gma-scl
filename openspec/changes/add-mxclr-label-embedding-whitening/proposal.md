## Why

MXCLR label embeddings are built from label descriptions and then used as the
semantic prior for label graph construction. Some experiments need an optional
whitening step on those label embeddings while preserving the existing default
behavior for reproducibility.

## What Changes

- Add a `whitening` runtime option to MXCLR label embedding construction.
- Keep `whitening=false` as the default and preserve the existing encoder call.
- Expose the option in MXCLR and MXCLRRank Hydra configs without adding a
  separate whitening epsilon setting.

## Impact

- Affected code: `src/models/loss/mxclr.py`, `src/models/loss/mxclr_rank.py`
- Affected configs: `configs/contrastive/model/mxclr.yaml`,
  `configs/contrastive/model/mxclr_rank.yaml`
- Affected tests: MXCLR loss/config tests
