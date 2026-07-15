## Why

classification stage の val/test では F1 と hamming loss は記録されますが、確率順位を反映する multi-label 指標である mAP が欠けています。checkpoint 選定指標は維持したまま、比較表と最終評価の両方で mAP を参照できるようにする必要があります。

## What Changes

- classification の validation と test で multilabel mAP を epoch 集計して記録する
- train/eval の統合テストに mAP 出力確認を追加する
- 評価契約を OpenSpec に追記し、val/test の標準指標集合に mAP を含める

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: classification stage の val/test 指標契約に multilabel mAP を追加する
- `evaluation`: train 経路で実行される classification test の標準出力指標に multilabel mAP を追加する

## Impact

- 変更対象: `src/models/finetune_module.py`, `tests/test_eval.py`, 関連 spec
- 依存影響: 既存の `torchmetrics` を利用するため新規依存追加なし
- 運用影響: checkpoint monitor は `classification/val/f1_macro` のまま維持する
