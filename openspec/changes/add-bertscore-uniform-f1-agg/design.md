## Context

The existing BERTScore graph builders compute a directional score by weighting each source label with `label_idf`. MXCLRRank consumes the resulting sample graph through the inherited MXCLR `score_graph()` path, so the clean integration point is the agg implementation and Hydra agg group rather than MXCLRRank itself.

## Decisions

### Add only the F1 uniform variant

The requested experiment needs F1 only. Do not add uniform Precision or Recall variants.

### Reuse BERTScore similarity construction

`BERTScore_F1_Uniform` reuses the existing SBERT/NPMI blended label similarity matrix and `transport_lambda`; it changes only source-label aggregation weights from `label_idf` to all-ones over active labels.

### Avoid loading IDF for the uniform variant

The new agg declares only `npmi` as required label statistic. MXCLR will therefore avoid computing `label_idf` for this variant.

## Risks

- Because active-label weights become uniform, rare labels no longer receive larger contribution through IDF. This is intended for ablation, not a replacement for the existing default.
- Existing W&B alias mapping must preserve the exact `BERTScore_F1_Uniform` canonical name or comparison columns will fragment.
