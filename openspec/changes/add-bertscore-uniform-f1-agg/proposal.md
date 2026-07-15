## Why

MXCLRRank currently has BERTScore F1 aggregation only with IDF-weighted source labels. To compare whether label-frequency-derived IDF weighting is beneficial, the experiment surface needs a BERTScore F1 variant that treats each active label equally.

## What Changes

- Add a new MXCLR-family agg choice `BERTScore_F1_Uniform`.
- Implement the new agg as BERTScore F1 with equal active-label weights instead of IDF weights.
- Keep the existing `BERTScore_F1` behavior unchanged.
- Expose the new agg through Hydra and W&B categorical aliases so MXCLRRank runs are comparable.
- Add an hparams_search entry that runs MXCLRRank with `BERTScore_F1_Uniform`.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `training`: MXCLR-family agg choices include an equal-label-weight BERTScore F1 option.

## Impact

- Affects `src/models/loss/agg/bertscore_f1.py`, `configs/contrastive/model/agg/`, `configs/hparams_search/`, MXCLR/MXCLRRank agg tests, W&B alias tests, and training specs.
