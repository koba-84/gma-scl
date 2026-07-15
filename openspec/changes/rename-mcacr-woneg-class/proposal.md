## Why

公開クラス名 `MCACR_WONEG` は全体命名ルールから外れるため、例外管理が必要になっています。命名規約を統一適用するため、アンダースコアを除去したクラス名へ移行して例外を廃止します。

## What Changes

- **BREAKING** `src.models.loss.mcacr_woneg.MCACR_WONEG` を `src.models.loss.mcacr_woneg.MCACRWONEG` へ改名する。
- `src/models/loss/__init__.py` の公開名と `__all__` を新クラス名へ更新する。
- `configs/contrastive/model/mcacr_woneg.yaml` の `_target_` を新クラス名へ更新する。
- 関連テスト・自己テスト・仕様記述を新クラス名へ更新する。
- Ruff 命名例外 `MCACR_WONEG` を削除し、命名ゲートを完全統一する。

## Capabilities

### New Capabilities
- なし

### Modified Capabilities
- `training`: built-in loss 公開クラス名を `MCACRWONEG` へ更新する。
- `python-naming-conventions`: クラス名例外運用を廃止する。
- `dev-quality-tooling`: 命名ゲートの例外設定を不要化する。

## Impact

- 影響コード: `src/models/loss/mcacr_woneg.py`, `src/models/loss/__init__.py`, `configs/contrastive/model/mcacr_woneg.yaml`, テスト参照ファイル
- 影響仕様: `openspec/specs/training/spec.md`, `openspec/specs/training.md`, `openspec/specs/python-naming-conventions/spec.md`
- 影響運用: 旧クラス名 import/target は非互換となるため、すべて新クラス名へ更新が必要
