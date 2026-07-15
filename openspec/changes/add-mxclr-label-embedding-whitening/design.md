## Context

MXCLR currently builds label embeddings by loading label descriptions and calling
`SentenceTransformer.encode(..., normalize_embeddings=True)`. The requested
change must keep that encoder path unchanged and only add an optional transform
after encoding.

## Decision

Add `whitening: bool = False` to MXCLR label embedding construction and public
MXCLR/MXCLRRank initializers. When disabled, `_build_label_embeddings` returns
the encoded tensor directly. When enabled, it centers the encoded matrix,
computes the feature covariance, applies an eigendecomposition-based whitening
matrix, and returns the transformed tensor.

The numerical clamp uses the same `1e-8` stability scale already used by loss
and aggregation components. It is an internal constant, not a Hydra setting.

## Non-goals

- Do not change `sbert_model_name` semantics.
- Do not add model-specific branches.
- Do not add Hugging Face AutoModel or AutoTokenizer pooling.
- Do not change MXCLR loss, aggregators, or label-statistic calculations.
