## Why

単体自己テストは整備されたが、pytest の統合テストでは sampler 切替や datamodule 経路の回帰を十分に捕捉できていない。ML プロジェクトの実務では、軽量な fast integration を常時実行し、重い学習統合は slow として分離する構成が推奨される。

## What Changes

- `tests/data_integration.py` を追加し、DataModule と sampler の統合経路を tiny データで検証する。
- 対象は `ClassificationDataModule` と `ContrastiveDataModule` とし、正常系と主要異常系を同時に検証する。
- `sampler_type=shuffle/gcbs/dpp` の切替に対する dataloader 挙動を統合テストで明示する。
- `openspec/specs/training.md` に統合テスト粒度（fast integration と slow integration の役割）を追記する。

## Capabilities

### Modified Capabilities

- `training`: 統合テスト層に DataModule/sampler の fast integration 要件を追加する。

## Impact

- 影響コード: `tests/data_integration.py`
- 影響仕様: `openspec/changes/add-data-integration-tests/specs/training/spec.md`, `openspec/specs/training.md`
- 影響運用: `uv run pytest -m "not slow"` で DataModule/sampler の統合回帰を常時検知できる。
