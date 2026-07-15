## Why

label overlap の OR/union 計算が `Base`、`MSC`、`MCACR` 系で別実装になっており、同じ意味の計算でも読み方が揺れています。loss 構成を揃えた直後なので、この重複も同じ基準で整理して helper ownership を明確にする必要があります。

## What Changes

- label overlap の OR-count / union-count 計算を `src/models/loss/components` の shared helper へ移す
- `Base` と `MSC` の `_compute_or`、`MCACR` / `MCACRWONEG` の同等 union 計算を shared helper ベースへ統一する
- 既存 test は shared helper への委譲を前提に維持し、重複した式を top-level loss module に残さない

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: contrastive loss modules の label overlap 計算 ownership を shared components に統一する

## Impact

- `src/models/loss/base.py`
- `src/models/loss/msc.py`
- `src/models/loss/mcacr.py`
- `src/models/loss/mcacr_woneg.py`
- `src/models/loss/components/`
- `tests/property_based.py`
- `tests/test_contrastive_losses.py`
- `openspec/specs/training.md`
- `openspec/specs/training/spec.md`
