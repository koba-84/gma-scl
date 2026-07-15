## ADDED Requirements

### Requirement: AAPD ラベル説明マッピング生成

This requirement MUST generate a mapping table between AAPD abbreviated labels and original arXiv taxonomy descriptions for training-time label embedding support.

#### Scenario: 単一スクリプトで 54 ラベルを生成できる

- **WHEN** 実行者が AAPD ラベル説明生成スクリプトを実行する
- **THEN** スクリプトは単一ファイル実装で完結して動作する
- **AND** 出力には AAPD 54 ラベルすべての略称と説明対応が含まれる

#### Scenario: 説明文は原文抽出である

- **WHEN** スクリプトが arXiv taxonomy を取得する
- **THEN** 説明文は要約や言い換えを行わず、抽出した原文を保存する

#### Scenario: 失敗時に中間生成物を残さない

- **WHEN** 取得または解析または保存処理の途中で失敗する
- **THEN** 途中生成された出力ファイルは削除される
