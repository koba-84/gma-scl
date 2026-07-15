## Context

MXCLR currently builds a soft sample graph from label descriptions using Sentence-BERT and an agg module, then trains embeddings with a soft-target contrastive objective. BERTScore_F1 already provides a symmetric positive semantic score in [0, 1], which is suitable as a neighborhood similarity source, but t-SNE expects smaller distances for closer neighbors and optimizes a KL divergence between high-dimensional affinities and low-dimensional Student t affinities.

## Goals / Non-Goals

**Goals:**

- Keep t-MXCLR close to MXCLR initialization and label-stat loading so datasets and label descriptions remain shared.
- Use openTSNE for the high-dimensional perplexity-based affinity construction.
- Avoid sign mistakes by converting BERTScore_F1 similarity to distance as `1 - score`.
- Make perplexity, exaggeration, and Student t degrees of freedom explicit config keys.
- Remove MCACR and MCACRWONEG without adding compatibility aliases.

**Non-Goals:**

- Do not implement an openTSNE optimizer inside the training loop.
- Do not retain deprecated MCACR import paths or Hydra targets.
- Do not alter unrelated contrastive losses.

## Decisions

1. t-MXCLR subclasses MXCLR and reuses its label embedding/stat initialization.
   - Rationale: the reference distribution still starts from the same label semantic graph, so duplicating loading logic would increase drift risk.
   - Alternative considered: a standalone class. Rejected because it would duplicate the data_dir/dataset_name/SBERT/agg contract.

2. The reference distribution P is built by openTSNE `PerplexityBasedNN` from a precomputed distance matrix.
   - Rationale: openTSNE owns the perplexity search and symmetrized affinity behavior, while BERTScore_F1 supplies the pairwise score matrix.
   - The distance matrix is `1 - BERTScore_F1`, with diagonal distance forced to zero.

3. The embedding distribution Q is computed in torch from squared L2 distances with a Student t kernel.
   - Rationale: gradients must flow through the model embeddings; openTSNE's optimizer is not a torch autograd component.
   - Formula uses `(1 + d2 / dof) ** (-(dof + 1) / 2)` over off-diagonal pairs, then normalizes to sum one.

4. Exaggeration scales P inside the KL objective.
   - Rationale: openTSNE applies exaggeration as a multiplier on attractive probabilities during optimization. t-MXCLR mirrors that effect by using `exaggeration * P` in the KL term.

## Risks / Trade-offs

- [Risk] openTSNE affinity construction runs on CPU per batch and adds overhead. -> Mitigation: the implementation only converts the fixed target graph to P, while the differentiable Q remains in torch.
- [Risk] Very small batches can make the configured perplexity too high. -> Mitigation: openTSNE lowers the effective perplexity according to its own check, and t-MXCLR still requires batch size at least 2.
- [Risk] MCACR removal breaks old configs. -> Mitigation: this is intentional under the repository policy of not keeping backward compatibility layers.
