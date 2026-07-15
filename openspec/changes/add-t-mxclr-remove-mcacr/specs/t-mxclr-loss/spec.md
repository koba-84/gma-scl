## ADDED Requirements

### Requirement: t-MXCLR loss availability

The repository MUST provide t-MXCLR as a selectable contrastive loss that reuses MXCLR label semantic initialization and BERTScore_F1 reference scoring.

#### Scenario: Resolve t-MXCLR target from config

- **WHEN** 開発者が `contrastive/model=t_mxclr` を compose する
- **THEN** `contrastive.model.loss_fn._target_` は `src.models.loss.t_mxclr.TMXCLR` として解決される
- **AND** `contrastive.model.loss_fn.agg._target_` は `src.models.loss.agg.bertscore_f1.BERTScoreF1Graph` として解決される
- **AND** `perplexity`, `exaggeration`, `degrees_of_freedom` は config に明示される

### Requirement: t-MXCLR reference distribution must use openTSNE perplexity affinities

t-MXCLR MUST convert the BERTScore_F1 sample graph to a high-dimensional t-SNE reference distribution using openTSNE perplexity-based affinities.

#### Scenario: Convert positive BERTScore_F1 similarities to distances

- **WHEN** t-MXCLR builds the reference distribution from labels
- **THEN** it first computes the BERTScore_F1 score graph through the MXCLR agg path
- **AND** it converts scores to distances with `distance = 1 - score`
- **AND** the diagonal distance is zero
- **AND** larger BERTScore_F1 values produce smaller reference distances

#### Scenario: Apply perplexity and exaggeration to the reference distribution

- **WHEN** t-MXCLR computes the KL objective
- **THEN** the reference distribution is produced by openTSNE `PerplexityBasedNN` with a precomputed distance matrix and the configured `perplexity`
- **AND** the KL attractive weights are multiplied by the configured `exaggeration`

### Requirement: t-MXCLR embedding distribution must use Student t over L2 distances

t-MXCLR MUST compute the learned embedding-side distribution from L2 embedding distances with a configurable Student t degrees-of-freedom parameter.

#### Scenario: Compute differentiable embedding-side distribution

- **WHEN** t-MXCLR receives embeddings `z`
- **THEN** it normalizes `z` consistently with MXCLR
- **AND** it computes pairwise squared L2 distances between normalized embeddings
- **AND** it applies a Student t kernel controlled by `degrees_of_freedom`
- **AND** self-pairs are excluded from normalization and loss calculation
- **AND** the returned loss is a finite differentiable scalar for a valid batch
