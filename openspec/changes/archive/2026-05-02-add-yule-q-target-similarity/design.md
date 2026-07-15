## Context

MXCLR target graph builders use label-description embeddings for cosine similarity and some agg modules additionally require train.csv-derived NPMI. The existing agg hyperparameter `transport_lambda` already controls the statistic-side weight: alpha is `1.0 - transport_lambda`, and the statistic component weight is `transport_lambda`.

## Goals / Non-Goals

**Goals:**

- Compute corrected pairwise Yule's Q from the same train.csv counts used by NPMI.
- Add one explicit hyperparameter, `yule_q_lambda`, for the beta term in `npmi + beta * yule_q`.
- Keep the existing `transport_lambda` interpretation as the cosine-vs-statistic blend weight.
- Cover MXCLR agg modules that already blend cosine with NPMI.

**Non-Goals:**

- Do not add a new agg choice or a runtime `similarity_type` switch.
- Do not change non-NPMI agg modules such as mean and chamfer.
- Do not add an external statistics dependency.

## Decisions

### Decision 1: Compute Yule's Q in label_stats from raw counts

Add `compute_yules_q(data_dir, dataset_name)` beside `compute_npmi`. For labels i and j, use a 2x2 table with Haldane-Anscombe correction: `a = pair_count + 0.5`, `b = count_i - pair_count + 0.5`, `c = count_j - pair_count + 0.5`, `d = n_docs - count_i - count_j + pair_count + 0.5`, then `Q = (a*d - b*c) / (a*d + b*c)`.

Alternative considered: compute odds ratios directly and transform later. Direct Q avoids infinities and gives a bounded matrix.

### Decision 2: Map Yule's Q to the same unit interval used by runtime NPMI

The runtime `compute_npmi` returns a `[0, 1]` matrix, so `compute_yules_q` will also return `((Q + 1) * 0.5).clamp(0, 1)` and set the diagonal to 1. This keeps `npmi + beta * yule_q` scale-compatible with existing target similarity code.

Alternative considered: expose raw `[-1, 1]` Q. That would mix differently scaled terms in existing agg modules and make beta harder to interpret.

### Decision 3: Reuse required_label_stats for Yule's Q

Agg modules with `yule_q_lambda > 0` will require the `yule_q` label statistic. MXCLR will validate the stat name and pass only requested stats into the agg call.

Alternative considered: always compute Yule's Q when NPMI is required. Conditional stats keep initialization cost tied to the configured hyperparameter.

## Risks / Trade-offs

- Statistic component can exceed 1 when beta is positive because the requested formula is `npmi + beta * yule_q`. Mitigation: clamp final similarity to the existing valid target range before downstream costs or graph scores.
- Existing `transport_lambda` name is less direct than alpha. Mitigation: keep config churn small and document that alpha is `1.0 - transport_lambda`.
