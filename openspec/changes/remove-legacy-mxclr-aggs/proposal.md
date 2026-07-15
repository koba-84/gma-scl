## Why

MXCLR agg choices include older mean and transport variants that are no longer part of the intended experiment surface. Keeping them selectable makes Hydra sweeps and reproducibility reviews ambiguous because unsupported aggregation families remain valid configuration choices.

## What Changes

- **BREAKING** Remove `mean`, `wmd`, `wrd`, `uot`, `chamfer`, and `idf_chamfer` as supported MXCLR-family agg choices.
- **BREAKING** Remove `t_mxclr` as a supported contrastive loss choice.
- Change MXCLR-family default aggs from removed choices to supported `BERTScore_F1`.
- Remove runtime modules, Hydra agg configs, tests, and specs that treat the removed aggs as supported choices.
- Keep `BERTScore_F1`, `BERTScore_Precision`, and `BERTScore_Recall` supported.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `training`: Supported MXCLR-family agg choices exclude `mean`, `wmd`, `wrd`, `uot`, `chamfer`, and `idf_chamfer`; `t_mxclr` is no longer a supported contrastive loss; MXCLR-family defaults resolve to a remaining supported agg.

## Impact

- Affects `configs/contrastive/model/agg/`, `configs/contrastive/model/mxclr.yaml`, MXCLR agg modules, MXCLR tests, config tests, W&B alias coverage tests, and training specs.
- Existing commands or sweeps that override removed agg names must be updated to a supported agg.
