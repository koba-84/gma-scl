## Context

`MXCLRRank` は `MXCLR` の soft-target contrastive loss に row-wise ListMLE を加算する。現状は `student_scores = (z @ z.T) / instance_temperature` としており、MXCLR 本体の logits 温度と ListMLE の順位スコア温度が結合している。

## Decisions

### Decision 1: ListMLE 専用温度名は `rank_temperature` とする

- 役割が ranking 項の score scaling であるため、`rank_temperature` として公開する。
- `instance_temperature` は `_compute_mxclr_loss` にだけ渡し、`rank_temperature` は `compute_listmle_loss` に渡す student score の scaling にだけ使う。
- `rank_temperature <= 0` は初期化時に `ValueError` とする。

### Decision 2: Hydra config は hidden default を持たない

- `configs/contrastive/model/mxclr_rank.yaml` に `rank_temperature` を明示する。
- 初期値は既存挙動を保つため `0.1` とする。

## Validation

- `uv run pytest tests/losses/test_mxclr_rank_loss.py tests/test_configs.py -q`
- `uv run pre-commit run -a`

## Risks

- 既存 sweep で `rank_temperature` を意識しない場合、初期値は旧 `instance_temperature=0.1` と同じため挙動は維持される。
