## Why

現状の MXCLR と MCACR の負例重み用ラベル類似度集約は全ペア平均（mean/self_norm）のみで、ラベル集合間の「最短対応」を重視する選択肢がありません。ラベル多重度が高いサンプル間で過度に平滑化されるため、Chamfer 的な近傍集約を導入して挙動比較できるようにします。

## What Changes

- MXCLR と MCACR の共通集約契約 `agg` に `chamfer` を追加する。
- `chamfer` は「各ラベルから相手集合内の最大類似度のみを取り、方向別平均を対称平均する」定義で実装する。
- MXCLR の `similarity_graph(labels)` と MCACR の repulsion 類似度集約の両方で同一の `chamfer` 定義を適用する。
- `configs/contrastive/model/mxclr.yaml` と `configs/contrastive/model/mcacr.yaml` で `agg: chamfer` を選択可能にする（既定値は変更しない）。
- 自己テストを更新し、`chamfer` 分岐の有限値性と既存分岐との差異を検証する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: contrastive loss の共通集約契約に `chamfer` 分岐を追加する。

## Impact

- 影響コード: `src/models/loss/mxclr.py`, `src/models/loss/mcacr.py`, `configs/contrastive/model/mxclr.yaml`, `configs/contrastive/model/mcacr.yaml`
- 影響仕様: `openspec/specs/training/spec.md`
- 追加依存はなし（既存 PyTorch 演算のみ）
