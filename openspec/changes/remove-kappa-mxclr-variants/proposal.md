## Why

The MXCLR experiment surface still includes `kappa`, `multi_scale_mxclr`, and `mxclr_kendall`, but these choices are no longer part of the intended comparison set. Removing them reduces config space and avoids keeping unused loss variants in reproducibility metadata.

## What Changes

- **BREAKING** Remove the `kappa` parameter and t-vMF learned-side similarity transform from MXCLR and MXCLRRank.
- **BREAKING** Remove `multi_scale_mxclr` as a selectable contrastive model and delete its implementation/tests/configs.
- **BREAKING** Remove `mxclr_kendall` as a selectable contrastive model and delete its implementation/tests/configs.
- Update tests and training specs so supported MXCLR-family losses are limited to the remaining runtime choices.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `training`: Remove `kappa`, `multi_scale_mxclr`, and `mxclr_kendall` from supported contrastive loss contracts.

## Impact

- Affects MXCLR and MXCLRRank loss APIs, Hydra configs, hyperparameter sweeps, config tests, loss tests, and OpenSpec training requirements.
- Existing overrides using `contrastive/model=multi_scale_mxclr`, `contrastive/model=mxclr_kendall`, or `contrastive.model.loss_fn.kappa` will fail instead of being accepted through compatibility aliases.
