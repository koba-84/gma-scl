## Why

classification stage の loss だけが `loss_name` と `loss_kwargs` の手組み分岐で解決されており、他の module と設定解決の流儀が揃っていない。Hydra instantiate に統一して、loss 追加時に module 側の分岐を増やさない構成へ寄せる。

## What Changes

- `FinetuneLitModule` は classification loss を `criterion` として直接受け取り、module 内の名前分岐を削除する。
- `configs/classification/loss/*.yaml` は `_target_` を持つ instantiate config に変更する。
- classification config テストを `criterion` config 前提に更新する。

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: classification finetune loss は Hydra instantiate 可能な config object として解決され、module 内の文字列分岐に依存しない

## Impact

- Affected code: `src/models/finetune_module.py`, `configs/classification/loss/*.yaml`, `tests/configs.py`
- APIs: `FinetuneLitModule` の init 引数は `loss_name`/`loss_kwargs` から `criterion` へ変更
- Dependencies: 追加依存なし
