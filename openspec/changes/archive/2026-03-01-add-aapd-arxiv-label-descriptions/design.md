## Overview

本変更は 1 ファイル完結の取得スクリプトで、AAPD の 54 ラベル略称と arXiv category taxonomy の説明文を対応付けた JSON を生成する。データ源は公開ページのみを利用し、説明文は原文を保持する。

## Data Sources

- AAPD ラベル順序: 既存公開実装で利用される 54 ラベル略称順序
- カテゴリ説明: arXiv category taxonomy ページ

## Extraction Strategy

1. AAPD の 54 略称ラベルを固定順で保持する。
2. arXiv taxonomy HTML を取得し、カテゴリ見出しと説明ブロックを抽出する。
3. 各ラベルについて以下を構築する。

- `index`: 1..54
- `label`: 略称（例: `cs.CL`）
- `taxonomy_title`: taxonomy 見出しの括弧内表示名
- `description`: taxonomy の説明原文（空の場合は空文字）

## Failure Handling

- 一時ファイルに書き出してからアトミックに rename する。
- 途中で例外が発生した場合は、一時ファイルと最終出力の両方を削除する。
- 54 ラベルすべてが taxonomy から見つからない場合は失敗として扱う。

## Output Format

- JSON 形式
- ルートにメタデータ（source URL, generated_at_utc, total_labels）
- `labels` 配列に 54 件の対応結果を格納
