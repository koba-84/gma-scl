## Why

AAPD データセットの現在のラベル列は 1..54 の数値で保持されており、arXiv 略称ラベルおよびカテゴリ説明を直接参照できない。ラベル埋め込みの精度を上げるため、略称ラベルと arXiv taxonomy の原文説明を機械的に対応付けて再利用可能にする必要がある。

## What Changes

- AAPD 54 ラベルの略称リストを固定順で定義し、arXiv category taxonomy からカテゴリ説明文を抽出する単一スクリプトを追加する。
- スクリプトは要約や言い換えを行わず、取得した原文説明をそのまま保存する。
- 取得・解析・保存の途中で失敗した場合、途中生成された出力ファイルを削除する。
- 出力として、列番号（1..54）と略称ラベル、カテゴリ名、説明文を持つ JSON を生成する。

## Capabilities

### New Capabilities

- `aapd-arxiv-label-descriptions`: AAPD ラベル略称と arXiv taxonomy 原文説明を対応付けたアーティファクトを再現可能に生成できる。

### Modified Capabilities

- `training`: 学習仕様に AAPD ラベル説明ファイル生成の前処理補助スクリプトを追加する。

## Impact

- 追加コード: scripts 配下の新規 Python スクリプト 1 ファイル
- 追加成果物: data/aapd 配下のラベル説明 JSON（生成物）
- 依存先: arxiv.org/category_taxonomy への HTTP アクセス
