## MODIFIED Requirements

### Requirement: Contrastive loss configuration must expose explicit runtime arguments

Contrastive loss configurations MUST declare every runtime initialization argument in Hydra config so reproducibility review does not require reading Python defaults. Supported contrastive loss configs MUST exclude removed MCACR and MCACRWONEG choices and include t-MXCLR and multi-scale MXCLR. NPMI-aware MXCLR agg configurations MUST expose only the runtime initialization arguments accepted by their aggregation implementations.

#### Scenario: Resolve contrastive loss configs without hidden defaults

- **WHEN** 開発者または coding agent が `configs/contrastive/model/*.yaml` を使って loss を解決する
- **THEN** each supported loss config contains every runtime initialization argument for its implementation
- **AND** `configs/contrastive/model/mxclr.yaml` exposes `data_dir`, `instance_temperature`, `graph_temperature`, `dataset_name`, `sbert_model_name`, `sbert_max_length`, `whitening`, and `agg`
- **AND** `configs/contrastive/model/mxclr_rank.yaml` exposes `data_dir`, `instance_temperature`, `graph_temperature`, `rank_temperature`, `lambda_rank`, `dataset_name`, `sbert_model_name`, `sbert_max_length`, `whitening`, and `agg`
- **AND** `configs/contrastive/model/t_mxclr.yaml` exposes `data_dir`, `instance_temperature`, `graph_temperature`, `perplexity`, `exaggeration`, `degrees_of_freedom`, `dataset_name`, `sbert_model_name`, `sbert_max_length`, and `agg`
- **AND** NPMI-aware MXCLR agg configs do not expose removed Yule's Q beta arguments
- **AND** MCACR, MCACRWONEG, multi-scale MXCLR, and MXCLR Kendall configs are not supported choices
