## MODIFIED Requirements

### Requirement: Contrastive loss configuration must expose explicit runtime arguments

Contrastive loss configurations MUST declare every runtime initialization argument in Hydra config so reproducibility review does not require reading Python defaults. Supported contrastive loss configs MUST exclude removed MCACR, MCACRWONEG, multi-scale MXCLR, and MXCLR Kendall choices. NPMI-aware MXCLR agg configurations MUST expose only the runtime initialization arguments accepted by their aggregation implementations.

#### Scenario: Resolve contrastive loss configs without hidden defaults

- **WHEN** 開発者または coding agent が `configs/contrastive/model/*.yaml` を使って loss を解決する
- **THEN** each supported loss config contains every runtime initialization argument for its implementation
- **AND** `configs/contrastive/model/mxclr.yaml` exposes `data_dir`, `instance_temperature`, `graph_temperature`, `dataset_name`, `sbert_model_name`, `sbert_max_length`, `whitening`, and `agg`
- **AND** `configs/contrastive/model/mxclr_rank.yaml` exposes `data_dir`, `instance_temperature`, `graph_temperature`, `rank_temperature`, `lambda_rank`, `dataset_name`, `sbert_model_name`, `sbert_max_length`, `whitening`, and `agg`
- **AND** `configs/contrastive/model/t_mxclr.yaml` exposes `data_dir`, `instance_temperature`, `graph_temperature`, `perplexity`, `exaggeration`, `degrees_of_freedom`, `dataset_name`, `sbert_model_name`, `sbert_max_length`, and `agg`
- **AND** NPMI-aware MXCLR agg configs do not expose removed Yule's Q beta arguments
- **AND** MCACR, MCACRWONEG, multi-scale MXCLR, and MXCLR Kendall configs are not supported choices

## REMOVED Requirements

### Requirement: Multi-scale MXCLR loss must use openTSNE multiscale affinities over MXCLR reference graphs

**Reason**: `multi_scale_mxclr` is removed from the supported contrastive loss surface.

**Migration**: Use one of the remaining contrastive model configs.

### Requirement: MXCLR rank and Kendall losses must support distinct ranking objectives with a single lambda coefficient

**Reason**: `mxclr_kendall` is removed from the supported contrastive loss surface. MXCLRRank remains as the supported ranking variant.

**Migration**: Use `contrastive/model=mxclr_rank` for the remaining ranking loss.

### Requirement: MXCLR learned embedding similarity must support t-vMF kappa

**Reason**: `kappa` is removed from MXCLR-family learned-side similarity.

**Migration**: Use the default normalized cosine learned-side similarity with no `kappa` config key.
