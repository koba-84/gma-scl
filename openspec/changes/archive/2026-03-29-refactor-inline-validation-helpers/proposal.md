## Why

単純な shape / column / config guard だけを行う private `validate` helper が点在しており、主要関数を読むときに前提条件を別箇所へ飛んで追う必要があります。pytest が整っている現在は、検証専用 helper を増やすより、前提チェックを主要関数内へ戻したほうが可読性が高いです。

## What Changes

- 単純な private `validate` helper を削除し、呼び出し元の主要関数へ inline する
- 対象は `finetune_module.py`, `mcacr.py` / `mcacr_woneg.py`, `transport.py`, `tokenized_dataset_cache.py`
- pytest は既存検証を維持しつつ、helper 削除後の経路で回帰を確認する

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: 単純な validation は helper 化せず主要関数内に保持する

## Impact

- `src/models/finetune_module.py`
- `src/models/loss/mcacr.py`
- `src/models/loss/mcacr_woneg.py`
- `src/models/loss/components/transport.py`
- `src/data/tokenized_dataset_cache.py`
- `tests/`
- `openspec/specs/training.md`
- `openspec/specs/training/spec.md`
