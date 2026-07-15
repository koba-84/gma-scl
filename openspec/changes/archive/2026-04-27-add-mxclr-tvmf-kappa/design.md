## Context

MXCLR computes its learned embedding-side distribution from normalized
embeddings with `z @ z.T`, then temperature-scales the result. MXCLRRank reuses
that MXCLR loss and also computes ListMLE student scores from the same learned
embedding cosine similarities. The reference-side `g_soft` graph is built by
`score_graph()` and agg modules, and must remain unchanged.

## Decisions

### Decision 1: Use a shared t-vMF similarity helper

Add a small helper that receives cosine similarities and `kappa` and returns:

```python
(1.0 + c) / (1.0 + kappa * (1.0 - c)) - 1.0
```

This keeps `kappa=0` exactly equivalent to cosine similarity and avoids a
runtime branch or `similarity_type` config.

### Decision 2: Expose only `kappa`

`kappa` is a non-negative scalar initialization argument. MXCLR and MXCLRRank
configs declare it explicitly for reproducibility. The default is `0.0` to
preserve existing behavior unless an experiment overrides it.

### Decision 3: Transform only learned embedding-side similarities

MXCLR applies the transform to the normalized embedding cosine matrix before
`instance_temperature` scaling. MXCLRRank applies the same transform to its
ListMLE student score cosine matrix before `rank_temperature` scaling. The
teacher/reference `g_soft` graph and agg modules are not modified.

## Validation

- Focused loss tests check the exact transform and `kappa=0` compatibility.
- Config tests check MXCLR and MXCLRRank expose the new runtime key.
- Pre-commit and branch policy gates run before commit/push.
