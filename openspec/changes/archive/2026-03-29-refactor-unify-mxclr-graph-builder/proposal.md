## Why

MXCLR の graph builder は similarity 系と transport 系で関数が分かれていますが、最終的に loss が必要とするのは sample-pair の soft target score 行列です。現状は matrix 構築、sample-pair 集約、MXCLR への受け渡しが family ごとに分かれて見通しが悪く、分岐の所在も読み取りづらくなっています。

## What Changes

- MXCLR の graph builder を 1 本化し、agg ごとの差は instantiate 設定だけで表現する
- similarity 系と transport 系は内部で別の集約 helper を使いながら、最終的には共通の score 行列へ正規化して loss に渡す
- MXCLR の公開 graph API は「類似度行列」ではなく「MXCLR が消費する score 行列」を返す契約へ揃える
- MXCLR の pytest を similarity 系と transport 系の両方で共通 score 契約を検証する形へ広げる

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: MXCLR graph builder を共通 score 契約に統一する

## Impact

- `src/models/loss/mxclr.py`
- `tests/property_based.py`
- `tests/test_contrastive_losses.py`
- `openspec/specs/training.md`
- `openspec/specs/training/spec.md`
