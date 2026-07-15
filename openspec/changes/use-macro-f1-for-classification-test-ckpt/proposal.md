## Why

classification stage の test では、checkpoint callback が選んだ best モデル重みを使用する。
現状の monitor は classification/val/f1_micro のため、ラベル不均衡時に少数ラベルの性能低下を見逃す可能性がある。
モデル重み選択基準を macro-F1 に変更し、各ラベルを等重みで評価したモデルを test に投入できるようにする。

## What Changes

- classification 用 model checkpoint monitor を classification/val/f1_macro に変更する。
- test で使用される重み選択基準が macro-F1 になっていることを設定テストで検証する。
- 評価仕様に checkpoint 選択基準（macro-F1）を追記する。

## Capabilities

### New Capabilities
- なし

### Modified Capabilities
- evaluation: classification test で使用する best checkpoint の選択基準を micro-F1 から macro-F1 へ変更する。

## Impact

- 影響コード: configs/callbacks/default.yaml, tests/configs.py
- 影響仕様: openspec/specs/evaluation/spec.md
- 依存追加なし
