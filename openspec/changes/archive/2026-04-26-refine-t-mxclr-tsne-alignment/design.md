## Context

`mxclr_rank` は `mxclr_kendall` への rename により公開設定から削除されたが、実験比較では旧名を残したまま新名も使いたい要件がある。現行の ranking 実体は differentiable Kendall tau であり、再導入する `mxclr_rank` は旧公開名とクラス名を復活させるだけで、数式は `mxclr_kendall` と揃える。

同時に、distill 系 agg が公開していた KoLeo regularizer は今後の実験対象から外れる。regularizer hook を loss 側に残すと、使わない挙動が暗黙に混入できるため、loss 側からも agg 側からも削除する。

## Decisions

### Decision 1: `mxclr_rank` は独立 module/class/config として復活させる

- `src.models.loss.mxclr_rank.MXCLRRank` を追加し、`MXCLRKendall` と同じ Kendall ranking objective を提供する。
- `configs/contrastive/model/mxclr_rank.yaml` を追加し、旧 `contrastive/model=mxclr_rank` override を再び解決可能にする。
- 後方互換レイヤーではなく、明示的な同等実装として管理する。

### Decision 2: regularizer hook は loss forward から削除する

- `MXCLR`, `MXCLRRank`, `MXCLRKendall`, `TMXCLR` は agg の `regularizer` attribute を参照しない。
- labels 経路と graph 直入力経路の差は score graph 構築の有無だけにする。

### Decision 3: 未使用 agg は公開選択肢から削除する

- `self_norm`, `distill_chamfer`, `distill_idf_chamfer` の Hydra config と Python agg module を削除する。
- distill 専用 helper は参照がなくなる場合に削除する。
- テストと spec は現行 supported agg のみを対象にする。

## Validation

- `uv run pytest tests/losses/test_mxclr_loss.py tests/losses/test_mxclr_kendall_loss.py tests/losses/test_mxclr_rank_loss.py tests/losses/test_t_mxclr_loss.py tests/property/test_mxclr_properties.py tests/test_configs.py -q`
- `uv run pre-commit run -a`
- GPU 前提の `scripts/test.sh` はローカルマシンで実行する。

## Risks

- `mxclr_rank` と `mxclr_kendall` の同等実装が将来分岐する可能性があるため、共有 helper と同等性テストで差分を検出する。
- distill/self_norm agg を参照する既存 sweep は失敗するため、削除を breaking change として spec と commit message に残す。
