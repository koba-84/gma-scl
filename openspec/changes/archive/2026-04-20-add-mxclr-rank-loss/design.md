# Design

## Context

main の `MXCLR` は agg object を受け取り、必要な label statistics を自動ロードして sample graph を構築する。`mxclr_rank` を追加する場合は、この契約を崩さずに `MXCLR` へ ranking 項だけを足すのが最小差分になる。

## Decisions

### Decision 1: MXCLRRank は MXCLR を継承して graph 構築経路を再利用する

- `MXCLRRank` は `MXCLR` を継承し、`score_graph()` と label statistics 初期化をそのまま使う。
- forward では `MXCLR` と同じ target shape 検証と regularizer 加算を維持しつつ、追加で ListMLE 項を計算する。
- これにより `idf_chamfer` や BERTScore 系を含む既存 agg config がそのまま使える。

### Decision 2: ranking 項は単一の lambda_rank で加算する

- 総損失は `mxclr_loss + lambda_rank * rank_loss` とする。
- `lambda_rank` は非負 scalar とし、`0` で ranking 無効化を表す。
- batch size による内部正規化は行わない。

Rationale:

- ハイパラの意味を設定値 1 個に集約できる。
- バッチサイズ変更時の寄与変化を暗黙に埋め込まないため、比較が明確になる。

### Decision 3: Hydra config は現行 MXCLR の naming policy に合わせる

- 温度キーは `instance_temperature` と `graph_temperature` を使う。
- ranking 係数は `lambda_rank` を明示する。
- agg 指定は `defaults` の `/contrastive/model/agg@loss_fn` を使い、`mxclr_rank` 固有の agg registry は作らない。

## Validation

- `uv run pytest tests/losses/test_mxclr_rank_loss.py tests/test_configs.py -q`
- `uv run pre-commit run -a`
