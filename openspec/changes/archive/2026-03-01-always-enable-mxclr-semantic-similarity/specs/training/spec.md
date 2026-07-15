## MODIFIED Requirements

### Requirement: MXCLR initialization must support AAPD semantic label similarity

MXCLR は AAPD 設定時に、ラベル説明文ファイルと Sentence-BERT モデル名を受け取り、初期化時にラベル間意味類似度行列を MUST 構築しなければならない。semantic 利用は MUST 常時有効であり、無効化オプションを持ってはならない。

#### Scenario: Build semantic label similarity at initialization

- **WHEN** 開発者が `dataset_name=aapd` と `label_description_path` を指定して `MXCLR` を初期化する
- **THEN** 説明文から Sentence-BERT 埋め込みを計算し、[L, L] の有限な類似度行列を保持する

#### Scenario: Fail fast on invalid semantic init config

- **WHEN** 説明ファイル不在またはラベル数不一致の設定で `MXCLR` を初期化する
- **THEN** MXCLR は学習開始前に明示的な例外を送出する
