## Context

`mxclr_rank` は ListMLE ranking 補助項を持つ旧実装名として復活させる意図だったが、復活時に `mxclr_kendall` と同じ helper をコピーしたため、`compute_diff_kendall_tau_loss` と `kendall_k` を使う実装になっている。

## Decisions

### Decision 1: MXCLRRank は ListMLE helper を使う

- `src.models.loss.components.listmle.compute_listmle_loss` を ranking 項に使う。
- `student_scores = (z @ z.T) / instance_temperature`、teacher は `g_soft`、mask は off-diagonal とする。
- `lambda_rank == 0` の場合は ranking 項を計算せず MXCLR loss だけを返す。

### Decision 2: MXCLRRank から Kendall 専用設定を削除する

- `MXCLRRank.__init__` と `configs/contrastive/model/mxclr_rank.yaml` から `kendall_k` を削除する。
- `MXCLRKendall` は `kendall_k` を維持し、Kendall tau 専用 loss として残す。

## Validation

- `uv run pytest tests/losses/test_mxclr_rank_loss.py tests/losses/test_mxclr_kendall_loss.py tests/test_configs.py -q`
- `uv run pre-commit run -a`

## Risks

- `mxclr_rank` の config key が変わるため、`kendall_k` を指定していた sweep は失敗する。これは `mxclr_rank` と `mxclr_kendall` の意味を分離するための意図的な修正である。
