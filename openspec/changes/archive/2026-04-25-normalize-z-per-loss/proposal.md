## Why

Contrastive embedding normalization is currently anchored in `ContrastiveLitModule._project`, so each loss implementation implicitly depends on caller-side preprocessing. This coupling makes loss behavior less portable and increases risk of divergence when losses are reused outside the module path.

## What Changes

- Move row-wise L2 normalization of `z` into each contrastive loss implementation (`Base`, `MulSupCon`, `MCACRLoss`, `MCACRWONEG`, `MXCLR`, `MXCLRKendall`, `MSC`) at loss computation time.
- Keep prototype normalization behavior explicit for MSC call sites while ensuring the loss side normalizes runtime `z` itself.
- Update related tests so each loss validates behavior with unnormalized inputs.
- Remove caller-side `z` normalization in `ContrastiveLitModule._project` for loss execution consistency.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `training`: Change contrastive-loss normalization contract so each loss normalizes `z` internally instead of depending on `ContrastiveLitModule._project`.

## Impact

- Affected code: `src/models/contrastive_module.py`, `src/models/loss/*.py`, and related loss tests under `tests/losses/`.
- No new runtime dependency is added.
- Behavior contract changes for contrastive loss execution path (normalization responsibility moves from caller to losses).
