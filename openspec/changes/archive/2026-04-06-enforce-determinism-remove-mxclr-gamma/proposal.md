## Why

本リポジトリは同一 commit・同一 Hydra 設定・同一 seed で同一結果を再現できることを最重要要件にしているが、現状の trainer 既定値は `deterministic: False` であり、利用者が明示 override を忘れると完全再現性を失う。加えて、MXCLR は focal-style weighting 用 `contrastive.model.loss_fn.gamma` を持つが、研究運用上の標準経路として維持する必然性がなく、設定・実装・仕様を複雑化させている。

## What Changes

- trainer の既定値を `deterministic: True` に変更し、contrastive/classification の両 stage が既定で deterministic 実行を継承するようにする。
- MXCLR と MXCLRRank から `gamma` 引数と focal-style weighting 実装を削除する。
- `configs/contrastive/model/mxclr.yaml` から `contrastive.model.loss_fn.gamma` を削除し、関連する Hydra 解決条件を更新する。
- MXCLR の unit/property/config テストを更新し、`gamma` 非依存の契約へ合わせる。
- main spec `openspec/specs/training/spec.md` を新契約へ同期する。

## Capabilities

### Modified Capabilities

- `training`: trainer 既定値の再現性要件を強化し、MXCLR loss 契約から `gamma` を除去する。

## Impact

- 影響コード: `configs/trainer/default.yaml`, `src/models/loss/mxclr.py`, `src/models/loss/mxclr_rank.py`
- 影響設定: `configs/contrastive/model/mxclr.yaml`
- 影響テスト: `tests/test_contrastive_losses.py`, `tests/test_property_based.py`, `tests/test_configs.py`
- 影響仕様: `openspec/specs/training/spec.md`
