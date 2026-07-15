## MODIFIED Requirements

### Requirement: MXCLR semantic initialization must be explicit and validated
MXCLR は `dataset_name=aapd` と `label_description_path` を指定して初期化し、Sentence-BERT でラベル間意味類似度行列を常時構築しなければならない。加えて、ラベル説明文エンコードの最大トークン長 `sbert_max_length` を明示設定で受け取り、初期化時に検証しなければならない。さらに、InfoNCE の batch 内候補 cross entropy に対する focal-style weighting 強度 `gamma` を設定で受け取り、`gamma>=0` を検証しなければならない。

#### Scenario: MXCLR applies configured SBERT max length
- **WHEN** 開発者が `MXCLR(..., sbert_model_name=..., sbert_max_length=256)` を初期化する
- **THEN** 実装は `SentenceTransformer.max_seq_length` に 256 を適用して説明文を encode する
- **AND** encode 後に意味類似度行列は有限値である

#### Scenario: MXCLR applies focal-style weighting to candidate cross entropy
- **WHEN** 開発者が `MXCLR(..., gamma=2.0)` を初期化し、標準経路で `forward(z, labels)` または `forward(z, g_soft)` を呼ぶ
- **THEN** 実装は batch 内候補確率 `p` から候補ごとに `(1 - p)^gamma` を計算する
- **AND** soft target 分布と負 log likelihood の積へその重みを適用して loss を集計する
- **AND** `gamma=0` のときは focal-style weighting なしの現行 CE と同じ loss を返す

#### Scenario: MXCLR rejects invalid gamma
- **WHEN** 開発者が `gamma<0` で MXCLR を初期化する
- **THEN** 実装は学習開始前に `ValueError` を送出する
