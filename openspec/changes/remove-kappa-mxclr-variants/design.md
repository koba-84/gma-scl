## Context

`kappa` currently changes the learned-side MXCLR similarity through a t-vMF transform. `multi_scale_mxclr` and `mxclr_kendall` are separate MXCLR-family loss variants with dedicated modules, configs, and tests. The repository policy disallows compatibility layers for removed research knobs, so deletion must remove public configs and Python APIs together.

## Goals / Non-Goals

**Goals:**

- Make MXCLR and MXCLRRank use normalized cosine similarity directly.
- Remove `kappa` from configs, constructors, helper functions, tests, and sweeps.
- Remove `multi_scale_mxclr` and `mxclr_kendall` implementations, configs, tests, and exports.
- Sync training specs with the reduced supported loss set.

**Non-Goals:**

- Do not remove `mxclr_rank` unless it is only an alias for the removed Kendall public choice.
- Do not change t-MXCLR or remaining agg behavior.
- Do not keep old config aliases or ignored constructor arguments.

## Decisions

1. Delete the `kappa` helper instead of forcing `kappa=0`.

   Rationale: retaining a forced-zero parameter would preserve a removed experiment axis and contradict runtime-argument config checks.

2. Delete variant modules and tests for removed model choices.

   Rationale: selectable contrastive model choices are the public experiment surface. Leaving importable classes for removed choices would make the surface ambiguous.

3. Keep MXCLRRank if it remains a supported distinct config.

   Rationale: the request names `mxclr_kendall`, not `mxclr_rank`. Existing specs still mention MXCLRRank separately, so only the named Kendall public choice is removed.

## Risks / Trade-offs

- Existing experiment commands using removed overrides will fail. → This is intentional and matches the no-backward-compatibility policy.
- Active OpenSpec changes may still mention removed choices. → Main specs and code will reflect the requested removal; unrelated active change docs are left untouched unless they block validation.
