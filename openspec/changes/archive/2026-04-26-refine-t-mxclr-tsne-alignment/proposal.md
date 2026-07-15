## Why

t-MXCLR 周辺の比較実験では、旧 `mxclr_rank` 名と新 `mxclr_kendall` 名を同時に選択できる必要がある。一方で、現行実験では regularizer 付き agg と distill/self_norm agg を使わないため、未使用の公開選択肢を残すと設定空間と再現性レビューが不要に広がる。

## What Changes

- `mxclr_rank` を `mxclr_kendall` と同時に使える公開 contrastive model として復活させる。
- `mxclr_rank` は旧 `MXCLRRank` 実装名を使い、既存 Kendall ranking ロジックと MXCLR agg group を再利用する。
- **BREAKING** contrastive loss から agg regularizer 加算経路を削除する。
- **BREAKING** `distill_chamfer`, `distill_idf_chamfer`, `self_norm` agg の config と実装を削除する。
- 関連 pytest と training main spec を更新し、対応 loss/agg の選択肢を明示する。

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: MXCLR-family loss の公開選択肢と対応 agg を更新し、regularizer 付き agg を非対応にする。

## Impact

- 影響コード: `src/models/loss/`, `src/models/loss/agg/`, `configs/contrastive/model/`, `tests/`
- 影響仕様: `openspec/specs/training/spec.md`
- 依存関係の追加はない。
