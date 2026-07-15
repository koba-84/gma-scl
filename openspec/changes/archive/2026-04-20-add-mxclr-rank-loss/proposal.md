## Why

main には teacher graph の行内順位を直接最適化する MXCLR 系 loss がない。
既存ブランチの `MXCLRRank` 案は main より古い API 前提で、そのまま merge すると現行の BERTScore agg 追加や温度パラメータ命名と衝突する。
また、ranking 項を batch size `m` で割る設計は、loss の寄与を設定値だけでは解釈しづらい。

## What Changes

- `src.models.loss.mxclr_rank.MXCLRRank` と row-wise ListMLE helper を追加する。
- `configs/contrastive/model/mxclr_rank.yaml` を追加し、現行の agg group override をそのまま使えるようにする。
- ranking 項の係数を単一の `lambda_rank` に統一し、内部で batch size 正規化しない。
- pytest と main spec を更新し、BERTScore 系 agg を含む `mxclr_rank` の利用可能性を検証する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: MXCLRRank を追加し、MXCLR agg group を再利用した ranking 補助項つき contrastive loss を使えるようにする

## Impact

- 影響コード: `src/models/loss/mxclr_rank.py`, `src/models/loss/components/listmle.py`, `configs/contrastive/model/mxclr_rank.yaml`
- 影響仕様: `openspec/specs/training/spec.md`, `openspec/specs/training.md`
- 実験運用: `lambda_rank` だけで ranking 項の寄与を制御でき、BERTScore 系 agg も `mxclr_rank` から選択できる
