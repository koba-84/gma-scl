## Why

MCACR と MXCLR の agg 分岐仕様が別々に定義されており、同一式の重複記載が発生している。重複は更新漏れと矛盾の原因になるため、共通契約へ統合して単一情報源化する。

## What Changes

- training の main spec に「共通集約契約」を追加する。
- MCACR/MXCLR の個別記述は共通契約参照へ置き換える。
- change specs でも重複式記述を共通契約参照へ合わせる。

## Capabilities

### New Capabilities

- `contrastive-aggregation-common-contract`: contrastive loss 間で共有する agg 分岐契約を定義する。

### Modified Capabilities

- `training`: MCACR/MXCLR の agg 仕様記述を共通契約参照形式へ変更する。

## Impact

- 影響仕様: openspec/specs/training.md, openspec/specs/training/spec.md
- 影響 change spec: add-mxclr-agg-branch, add-mcacr-agg-branch
