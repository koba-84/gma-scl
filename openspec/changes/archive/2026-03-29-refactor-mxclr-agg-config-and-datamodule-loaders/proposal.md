## Why

MXCLR の agg family ごとの差分は Hydra config で表現できる内容なのに、現状は `MXCLR_GRAPH_BUILDERS` という Python dict に閉じ込められています。これでは agg の責務が config から読めず、`mxclr.yaml` の `agg` 値と Python 側 registry の二重管理になっています。

また tokenized datamodule は `train_dataloader` が各 subclass、`val_dataloader` / `test_dataloader` が base class に分散しており、LightningDataModule として読むと公開 loader の所在が不自然です。共通処理は helper に残しつつ、各 datamodule で train/val/test を揃えて宣言した方が標準的です。

## What Changes

- `configs/contrastive/model/agg/` を追加し、MXCLR agg ごとの差分を Hydra config group へ移す
- `configs/contrastive/model/mxclr.yaml` は agg group を defaults で読む形にし、Python 側の `MXCLR_GRAPH_BUILDERS` registry を削除する
- `MXCLR` は config から注入された graph builder callable を直接使う
- tokenized datamodule base は dataloader helper を提供するだけに寄せ、classification / contrastive の各 module が train/val/test を揃えて持つ形へ整理する
- 関連 pytest と OpenSpec main specs を更新する

## Capabilities

### Modified Capabilities

- `training`: MXCLR agg family の選択を Hydra config group で解決する
- `tokenized-datamodule-layout`: 各 datamodule が train/val/test loader を同じ module 内に揃えて定義する

## Impact

- `configs/contrastive/model/mxclr.yaml`
- `configs/contrastive/model/agg/*.yaml`
- `src/models/loss/mxclr.py`
- `src/data/tokenized_datamodule_base.py`
- `src/data/classification_datamodule.py`
- `src/data/contrastive_datamodule.py`
- `tests/configs.py`
- `tests/data_integration.py`
- `tests/property_based.py`
- `tests/test_contrastive_losses.py`
- `openspec/specs/training.md`
- `openspec/specs/training/spec.md`
- `openspec/specs/tokenized-datamodule-layout/spec.md`
