## Context

The current agg group exposes both active semantic aggregations and older mean/transport implementations. The user request is removal, not deprecation, and the project policy disallows compatibility layers for old behavior.

## Decisions

### Remove the public config surface

Delete `mean.yaml`, `wmd.yaml`, `wrd.yaml`, `uot.yaml`, `chamfer.yaml`, and `idf_chamfer.yaml` from the Hydra agg group. Because MXCLR-family configs currently default to removed aggs, switch them to `BERTScore_F1`, which is already supported by MXCLR, MXCLRRank tests, and the label-stat autoload path.

### Remove runtime implementations and direct test usage

Delete the corresponding concrete agg modules and remove imports/parameterization from tests. This keeps unsupported choices from being available through Python direct construction even when Hydra configs are absent.

### Remove t-MXCLR

Delete the `t_mxclr` Hydra config, implementation module, hparam-search config, tests, and specs. The remaining supported MXCLR-family loss surface is MXCLR and MXCLRRank.

### Keep shared transport helper code untouched

Do not remove `src/models/loss/components/transport.py` in this change. The request is specifically about agg choices, and removing the helper would be a broader cleanup with different blast radius.

## Risks

- Existing hparam search configs or external scripts may still reference removed agg names and will fail at compose time.
- Active uncommitted changes overlap the same files, so commit staging must be limited carefully to this change.
