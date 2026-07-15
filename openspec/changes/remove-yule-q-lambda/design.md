## Context

MXCLR NPMI-aware aggregation currently accepts `yule_q_lambda` in Hydra configs and Python constructors, conditionally requests the `yule_q` label statistic, and blends that statistic into the target label graph. The project policy disallows keeping compatibility layers for removed research knobs, so removal must be explicit across configs, implementation, tests, and specs.

## Goals / Non-Goals

**Goals:**

- Remove `yule_q_lambda` from the public MXCLR aggregation surface.
- Make NPMI-aware aggregation use the existing cosine/NPMI blend only.
- Keep config resolution and targeted loss tests aligned with the reduced constructor signatures.

**Non-Goals:**

- Do not remove unrelated label-statistic utilities unless they become unreferenced by the codebase and tests.
- Do not introduce aliases, deprecation warnings, or fallback parsing for old configs.
- Do not change non-MXCLR loss behavior.

## Decisions

1. Remove the constructor argument instead of ignoring it.

   Rationale: the repository explicitly rejects backward compatibility for removed behavior, and accepting an ignored argument would keep the old experiment surface ambiguous.

   Alternative considered: keep `yule_q_lambda` with a forced zero value. This was rejected because it preserves a removed hyperparameter in configs and review output.

2. Route only NPMI through NPMI-aware aggs.

   Rationale: MXCLR already has `required_label_stats` as the runtime contract for statistics. Removing the Yule's Q branch there prevents unnecessary train-label statistic computation.

   Alternative considered: always compute Yule's Q but do not pass it. This was rejected because it creates unused compute and contradicts the public signature requirement.

3. Update specs and tests in the same change.

   Rationale: the current main specs require `yule_q_lambda`, so implementation without spec changes would leave the repository internally inconsistent.

## Risks / Trade-offs

- Existing experiment configs containing `yule_q_lambda` will fail to instantiate. → This is intentional for a breaking removal and keeps reproducibility metadata honest.
- Yule's Q utility code may remain if still independently tested. → Only public/runtime usage is removed; dead-code removal is based on actual references.
