## Context

Current contrastive training normalizes projected embeddings in `ContrastiveLitModule._project` before dispatching to loss functions. This creates a hidden caller-side dependency for loss implementations, and loss behavior can diverge when reused from tests or alternative call paths that bypass the module.

## Goals / Non-Goals

**Goals:**
- Make each contrastive loss self-contained by normalizing runtime `z` internally.
- Remove implicit dependence on caller-side embedding normalization for loss correctness.
- Preserve existing public loss APIs and keep prototype handling semantics for MSC.

**Non-Goals:**
- No redesign of objective formulas or aggregation logic.
- No compatibility layer that supports both old and new normalization ownership.
- No changes to non-contrastive losses.

## Decisions

1. Normalize `z` in each contrastive loss `forward` path or its private compute helper using `torch.nn.functional.normalize(..., dim=1)`.
   - Rationale: keeps normalization colocated with the objective and avoids duplicating call-site assumptions.
   - Alternative considered: keep normalization in `ContrastiveLitModule` and only add safety normalization in selected losses. Rejected because it preserves split responsibility and hidden coupling.

2. Stop normalizing `z` in `ContrastiveLitModule._project`.
   - Rationale: prevents dual ownership and makes module output represent raw projection head output.
   - Alternative considered: leave module normalization and accept redundant normalization in losses. Rejected because it hides ownership and keeps behavior dependent on call path.

3. Update loss tests to assert stable behavior from unnormalized inputs.
   - Rationale: test contract should validate new ownership and prevent regressions.

## Risks / Trade-offs

- **Risk:** Dynamic sampler refresh now consumes unnormalized projected embeddings if it uses `_project` output. → **Mitigation:** keep change scoped to loss contract and validate existing tests that exercise module/runtime paths.
- **Risk:** Numeric outputs of some loss unit tests change after moving normalization ownership. → **Mitigation:** update expected-value tests to use normalized reference logic where required.
