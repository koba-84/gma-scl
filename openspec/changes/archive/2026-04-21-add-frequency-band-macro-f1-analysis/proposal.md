## Why

classification test prediction artifact は保存されるようになったが、ラベル頻度に応じた性能差を同じ入力から再現計算する手段がない。AAPD の長尾ラベルでモデル差を確認できるよう、label frequency に基づく頻度帯別 Macro-F1 集計を標準化する。

## What Changes

- AAPD train split の label frequency を使ってラベルを 4 つの頻度帯へ分割し、各帯の label-wise F1 平均を算出する分析スクリプトを追加する
- 保存済み prediction artifact から score と target を読み込み、既存 classification test と同じ 0.5 閾値で二値化して再計算する
- 集計結果にはモデルごとの overall Macro-F1 と各頻度帯の Macro-F1、各帯のラベル数と頻度範囲を含める

## Capabilities

### New Capabilities
- `prediction-analysis`: 保存済み classification prediction artifact から頻度帯別 Macro-F1 を再計算する分析契約

### Modified Capabilities

## Impact

- 影響コード: scripts/a.py
- 影響仕様: openspec/specs/prediction-analysis/spec.md
- 依存追加なし
