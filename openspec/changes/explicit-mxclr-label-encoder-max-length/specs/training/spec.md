## MODIFIED Requirements

### Requirement: MXCLR semantic initialization must be explicit and validated
MXCLR は `dataset_name=aapd` と `label_description_path` を指定して初期化し、Sentence-BERT でラベル間意味類似度行列を常時構築しなければならない。加えて、ラベル説明文エンコードの最大トークン長 `sbert_max_length` を明示設定で受け取り、初期化時に検証しなければならない。

#### Scenario: MXCLR applies configured SBERT max length
- **WHEN** 開発者が `MXCLR(..., sbert_model_name=..., sbert_max_length=256)` を初期化する
- **THEN** 実装は `SentenceTransformer.max_seq_length` に 256 を適用して説明文を encode する
- **AND** encode 後に意味類似度行列は有限値である

#### Scenario: MXCLR rejects invalid max length
- **WHEN** 開発者が `sbert_max_length<=0` で MXCLR を初期化する
- **THEN** 実装は学習開始前に `ValueError` を送出する
