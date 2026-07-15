## Context

`scripts/a.py`, `scripts/b.py`, and `scripts/c.py` currently map each model name to one unsuffixed prediction artifact path. Multi-seed experiment summaries require either manual averaging outside the repository or overwriting files, both of which weaken reproducibility.

## Goals / Non-Goals

**Goals:**

- Load prediction artifacts named with an integer seed suffix, for example `bce0.pt`.
- Compute existing overall and frequency-band Macro-F1 metrics per seed artifact.
- Report both seed-level rows and model rows as arithmetic means across discovered seed artifacts.
- Keep the existing band construction and metric implementation unchanged.

**Non-Goals:**

- Do not average raw prediction tensors across seeds.
- Do not introduce CLI configuration for seed lists until there is a concrete need.
- Do not keep compatibility with unsuffixed artifact filenames.

## Decisions

- Discover artifacts with a glob pattern per model prefix, then sort by parsed integer seed. This avoids hard-coding the number of seeds while keeping output deterministic.
- Treat a filename as valid only when the part after the model prefix is all digits. This prevents files such as `bce_best.pt` from being silently included.
- Print seed-level metric rows after each seed artifact is evaluated, then average metric dictionaries for the model-level summary. This preserves both individual repeated-experiment metrics and the semantics of "multi-seed average" as the mean of repeated experiment metrics.

## Risks / Trade-offs

- Missing seed files can produce means over different seed counts per model. The scripts will print a `seed_count` column so this is visible.
- Glob discovery can pick up stale files if they match the seed-suffix pattern. Users must keep each `tmp/pred/<dataset>/` directory scoped to the intended experiment set.
