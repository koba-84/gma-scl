## Why

MCACR and MCACRWONEG are no longer part of the target contrastive loss set, while the experiment plan needs a t-SNE-aligned MXCLR variant that connects semantic label similarity and embedding geometry more directly. This change removes the obsolete MCACR selectable paths and introduces t-MXCLR with explicit, reproducible t-SNE distribution controls.

## What Changes

- **BREAKING**: Remove MCACR and MCACRWONEG loss implementations, exports, tests, and Hydra model configs.
- Add t-MXCLR as a selectable contrastive loss that follows MXCLR label-graph initialization.
- Add openTSNE as a runtime dependency for perplexity-based reference distribution construction.
- Use BERTScore_F1 as the t-MXCLR reference similarity source and convert it to a t-SNE high-dimensional probability distribution with explicit perplexity control.
- Use a Student t distribution over L2 embedding distances for the learned embedding-side distribution, with configurable degrees of freedom.
- Expose t-MXCLR perplexity, exaggeration, and degrees-of-freedom hyperparameters in Hydra config.

## Capabilities

### New Capabilities

- `t-mxclr-loss`: t-SNE-style MXCLR loss behavior, configuration, and reproducibility contract.

### Modified Capabilities

- `training`: Remove MCACR/MCACRWONEG as supported contrastive loss choices and add t-MXCLR to the supported MXCLR family.
- `mcacr-woneg-loss`: Retire the MCACRWONEG availability requirement because the implementation is removed.

## Impact

- `pyproject.toml` and `uv.lock` add openTSNE.
- `src/models/loss/` removes MCACR files and adds t-MXCLR.
- `configs/contrastive/model/` removes MCACR configs and adds t-MXCLR config.
- Tests and W&B config aliases are updated to match the supported loss set.
