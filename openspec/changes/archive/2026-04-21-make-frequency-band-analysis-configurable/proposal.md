## Why

頻度帯別 Macro-F1 の分析は有用だが、現状は 4 分位固定かつ手実装 F1 なので、比較したい頻度境界を都度指定できない。研究用途の再現分析として、`torchmetrics` に基づく指標計算と、ユーザー指定の頻度帯境界を使う契約へ揃える必要がある。

## What Changes

- `scripts/a.py` の Macro-F1 再計算を `torchmetrics` ベースへ変更する
- 頻度帯を固定 4 分位ではなく、CLI 引数で指定した frequency boundary から構築できるようにする
- 指定がない場合だけ既定の 4 分位境界を train label frequency から計算して使う
- prediction analysis spec を固定 4 分位前提から configurable boundary 前提へ更新する

## Capabilities

### New Capabilities

### Modified Capabilities
- `prediction-analysis`: 頻度帯別 Macro-F1 分析を `torchmetrics` と user-specified boundaries に基づく契約へ変更する

## Impact

- 影響コード: scripts/a.py
- 影響仕様: openspec/specs/prediction-analysis/spec.md
- 依存追加なし
