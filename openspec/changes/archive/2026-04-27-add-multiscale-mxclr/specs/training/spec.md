## ADDED Requirements

### Requirement: Multi-scale MXCLR loss availability

The repository MUST provide multi-scale MXCLR as a selectable contrastive loss that reuses MXCLR label semantic initialization and BERTScore_F1 reference scoring.

#### Scenario: Resolve multi-scale MXCLR target from config

- **WHEN** 開発者が contrastive/model=multi_scale_mxclr を compose する
- **THEN** contrastive.model.loss_fn._target_ は src.models.loss.multi_scale_mxclr.MultiScaleMXCLR として解決される
- **AND** contrastive.model.loss_fn.agg._target_ は src.models.loss.agg.bertscore_f1.BERTScoreF1Graph として解決される
- **AND** perplexities と exaggeration は config に明示される
- **AND** instance_temperature と graph_temperature は config に含まれない

### Requirement: Multi-scale MXCLR reference distribution must use openTSNE Multiscale affinities

Multi-scale MXCLR MUST convert the BERTScore_F1 sample graph to a high-dimensional t-SNE reference distribution using openTSNE multi-perplexity affinities.

#### Scenario: Apply multi-scale perplexities to the reference distribution

- **WHEN** multi-scale MXCLR computes the KL objective
- **THEN** it first computes the BERTScore_F1 score graph through the MXCLR agg path
- **AND** it converts scores to distances with distance = 1 - score
- **AND** the diagonal distance is zero
- **AND** the reference distribution is produced by openTSNE Multiscale with a precomputed distance matrix and the configured perplexities
- **AND** the KL attractive weights are multiplied by the configured exaggeration

### Requirement: Multi-scale MXCLR embedding distribution must use unnormalized L2 Gaussian affinities

Multi-scale MXCLR MUST compute the learned embedding-side distribution from unnormalized embedding L2 distances with a Gaussian kernel and no MXCLR temperature scaling.

#### Scenario: Compute differentiable unnormalized L2 Gaussian embedding-side distribution

- **WHEN** MultiScaleMXCLR receives embeddings z
- **THEN** it computes pairwise squared L2 distances from z without row-wise normalization
- **AND** it applies a Gaussian log-kernel with temperature scaling fixed to 1
- **AND** self-pairs are excluded from log normalization and loss calculation
- **AND** the returned loss is a finite differentiable scalar for a valid batch
