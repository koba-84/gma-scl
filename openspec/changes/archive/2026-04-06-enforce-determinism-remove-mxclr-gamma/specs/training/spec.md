## MODIFIED Requirements

### Requirement: Training execution environment

Training workflows MUST run in the uv virtual environment, SHALL execute commands through uv run, and SHALL default to deterministic trainer execution for reproducible runs.

#### Scenario: Execute training entrypoint in uv environment

- **WHEN** 開発者が学習を実行する
- **THEN** train エントリポイントは `uv run python src/train.py` 形式で起動される

#### Scenario: Resolve deterministic trainer default

- **WHEN** 開発者が `uv run python src/train.py --cfg job --resolve` を実行する
- **THEN** top-level `trainer.deterministic` は `True` として解決される
- **AND** `contrastive.trainer.deterministic` と `classification.trainer.deterministic` はその既定値を継承する

### Requirement: MXCLR semantic initialization must be explicit and validated

MXCLR MUST resolve label descriptions from `data_dir` and `dataset_name`, build label embeddings with Sentence-BERT, validate `sbert_max_length` at initialization, and exclude focal-style weighting `gamma` from its public contract and resolved Hydra configuration.

#### Scenario: MXCLR applies configured SBERT max length

- **WHEN** 開発者が `MXCLR(..., sbert_model_name=..., sbert_max_length=256)` を初期化する
- **THEN** 実装は `SentenceTransformer.max_seq_length` に 256 を適用して説明文を encode する
- **AND** encode 後に意味類似度行列は有限値である

#### Scenario: MXCLR computes loss without gamma override

- **WHEN** 開発者が `MXCLR(..., tau=..., tau_s=..., agg=...)` を初期化し、標準経路で `forward(z, labels)` または `forward(z, g_soft)` を呼ぶ
- **THEN** 実装は soft target 分布と候補 log probability から batch 内候補 cross entropy を集計する
- **AND** 公開初期化引数に `gamma` は存在しない
- **AND** Hydra 設定キー `contrastive.model.loss_fn.gamma` は解決対象に含まれない
