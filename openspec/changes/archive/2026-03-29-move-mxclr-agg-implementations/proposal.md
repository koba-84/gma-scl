## Why

現在の `src/models/loss/mxclr.py` は loss 本体に加えて agg 実装とその helper まで抱えており、責務が混ざっています。MXCLR の loss 本体と agg 実装は別 concern なので、配置も分けるべきです。

## What Changes

- `src/models/loss/agg/` ディレクトリを追加する
- MXCLR の concrete agg 実装と関連 helper を `loss/agg` 配下へ移す
- `mxclr.py` は loss 本体と label description / embedding 初期化に関する処理だけへ絞る
- config と tests の import / `_target_` を新しい配置へ更新する

## Capabilities

### Modified Capabilities

- `training`: MXCLR agg 実装は loss 本体から分離され、`loss/agg` 配下で管理される

## Impact

- `src/models/loss/mxclr.py`
- `src/models/loss/agg/*.py`
- `src/models/loss/components/transport.py`
- `configs/contrastive/model/agg/*.yaml`
- `tests/property_based.py`
- `tests/test_contrastive_losses.py`
- `openspec/specs/training/spec.md`
