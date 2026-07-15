## Purpose

Define reproducible training execution rules, stage contracts, and validation workflow for this repository.
## Requirements
### Requirement: Training execution environment

Training workflows MUST run in the uv virtual environment, and SHALL execute commands through uv run.

#### Scenario: Execute training entrypoint in uv environment

- **WHEN** 開発者が学習を実行する
- **THEN** train エントリポイントは `uv run python src/train.py` 形式で起動される

### Requirement: Dependency updates must use uv add

Dependency updates for training workflows MUST be performed with `uv add` commands, and project documentation MUST NOT instruct dependency installation via pip or conda.

#### Scenario: Add runtime dependency for training

- **WHEN** 開発者が学習関連の実行時依存を追加する
- **THEN** `uv add <package>` を使用する

#### Scenario: Add non-runtime dependency for training

- **WHEN** 開発者が学習関連の開発依存または追加機能依存を追加する
- **THEN** `uv add --group dev <package>` を使用する

#### Scenario: Add Ruff as development dependency

- **WHEN** 開発者が Python 品質チェック基盤として Ruff を導入する
- **THEN** `uv add --group dev ruff` を使用する

### Requirement: Stage defaults in train config

The train configuration SHALL include both contrastive and classification stages by default.

#### Scenario: Resolve default train config

- **WHEN** 開発者が `uv run python src/train.py --cfg job --resolve` を実行する
- **THEN** 設定に contrastive と classification の両方が含まれる
- **AND** classification.model の損失設定を解決してインスタンス化できる

### Requirement: Classification stage default epoch budget

The default classification stage configuration MUST cap `classification.trainer.max_epochs` at `40`.

#### Scenario: Resolve classification default max epochs

- **WHEN** 開発者が `uv run python src/train.py --cfg job --resolve` を実行する
- **THEN** `classification.trainer.max_epochs` は `40` として解決される

### Requirement: Classification stage must log standard validation and test metrics

classification stage MUST record both threshold-based and ranking-based val/test metrics at epoch granularity. multilabel mAP は sigmoid 後の score を入力として記録し、既存の checkpoint monitor は維持する。

#### Scenario: Log validation metrics including mAP

- **WHEN** 開発者または coding agent が classification stage の validation を実行する
- **THEN** `classification/val/f1_macro`, `classification/val/f1_micro`, `classification/val/hamming_loss`, `classification/val/map` が epoch metric として記録される
- **AND** `classification/val/map` は二値化後予測ではなく sigmoid score から計算される

#### Scenario: Log test metrics including mAP

- **WHEN** 開発者または coding agent が classification stage の test を実行する
- **THEN** `classification/test/f1_macro`, `classification/test/f1_micro`, `classification/test/hamming_loss`, `classification/test/map` が epoch metric として記録される
- **AND** 空テキスト補正は F1/hamming loss 用の二値予測にだけ適用され、mAP 用 score は順位情報を保持する

#### Scenario: Log classification epoch metrics via MetricCollection

- **WHEN** 開発者または coding agent が classification stage の validation/test metric 実装を更新する
- **THEN** 同一入力を共有する epoch 指標群は `torchmetrics.MetricCollection` として管理される
- **AND** epoch end の記録は `self.log_dict()` でまとめて行われる

#### Scenario: Keep non-collection metrics on explicit `self.log()`

- **WHEN** 開発者または coding agent が classification stage の metric logging を実装する
- **THEN** `classification/epoch` や validation loss のような collection 化しない値だけ個別 `self.log()` を使う
- **AND** collection 化できる metric は個別 `self.log()` に戻さない

#### Scenario: Persist classification test score-target pairs as a W&B artifact

- **WHEN** 開発者または coding agent が W&B logger 付きで classification stage の test を実行する
- **THEN** test 中に計算した sigmoid score と正解ラベルの全ペアは単一の W&B artifact file として保存される
- **AND** artifact だけから `classification/test/map` などの test 指標を再計算できる

#### Scenario: Skip test prediction artifact logging without a W&B run

- **WHEN** 開発者または coding agent が W&B logger なしで classification stage の test を実行する
- **THEN** classification test metric logging は従来どおり完了する
- **AND** W&B artifact 保存処理は呼び出されない

### Requirement: W&B hyperparameter config must use resolved values

When training logs hyperparameters to W&B, the exported config MUST use interpolation-resolved values rather than raw Hydra `${...}` references. For the currently executing stage, the exported stage config MUST reflect the stage-effective merged runtime configuration rather than the pre-merge base config. The same export MUST include deterministic comparison aliases for contrastive/classification losses and MXCLR-family settings so dashboard columns remain stable across live logging and backfill updates.

#### Scenario: Log resolved trainer references to W&B

- **WHEN** 開発者または coding agent が logger 付きで hyperparameters を記録する
- **THEN** W&B に送る `contrastive` や `classification` の config には `${trainer.accelerator}` のような未解決参照が残らない
- **AND** `classification.trainer.accelerator` のような値は実際の compose 結果である `gpu` や `cpu` として記録される

#### Scenario: Log stage-effective merged config to W&B

- **WHEN** 開発者または coding agent が stage-local override を含む `contrastive` または `classification` stage を実行する
- **THEN** W&B に送る当該 stage の config は top-level `trainer` と stage-local `trainer` を merge した実効値を記録する
- **AND** stage 実行時に使われた `max_epochs` や optimizer/loss の override 値は空欄にならない

#### Scenario: Log flat aliases for nested hyperparameters

- **WHEN** 開発者または coding agent が nested config を W&B へ記録する
- **THEN** `contrastive.model.loss_fn.graph_temperature` や `classification.model.optimizer.lr` のような leaf 値は dot-path key としても記録される
- **AND** W&B 比較列で参照する主要 hyperparameter が空欄のまま残らない

#### Scenario: Log derived loss-name aliases

- **WHEN** 開発者または coding agent が現行 config から loss 実装を一意に特定できる run を W&B へ記録する
- **THEN** `contrastive.model.loss_name` は `_target_` の module 名から導出した値として記録される
- **AND** `classification.model.loss_name` は criterion `_target_` から導出した値として記録される

#### Scenario: Log derived MXCLR agg and graph_temperature aliases

- **WHEN** 開発者または coding agent が MXCLR または MXCLR_PROTO の config を W&B へ記録する
- **THEN** `contrastive.model.loss_fn.agg_name` は `loss_fn.agg._target_` から比較用 alias として記録される
- **AND** `contrastive.model.loss_fn.graph_temperature` が config leaf に無い MXCLR_PROTO run では `graph_temperature_schedule.start` を比較用 alias として記録できる

#### Scenario: Log categorical choices under stable `*_name` aliases

- **WHEN** 開発者または coding agent が implementation-backed な有限選択肢を含む config を W&B へ記録する
- **THEN** contrastive/classification loss や MXCLR agg の比較用 alias は `*_name` leaf に記録される
- **AND** structured config subtree 自体は比較 alias によって上書きされない

#### Scenario: Cover every supported categorical choice with tests

- **WHEN** 開発者または coding agent が W&B categorical alias 実装を更新する
- **THEN** `configs/contrastive/model/*.yaml` `configs/contrastive/model/agg/*.yaml` `configs/classification/loss/*.yaml` の support 対象選択肢は pytest で総当たり検証される
- **AND** 各選択肢は W&B comparison で使う canonical alias 名として記録される

#### Scenario: Keep live logging and backfill alias derivation equivalent

- **WHEN** 開発者または coding agent が runtime logging と backfill の両方で alias 補完を行う
- **THEN** 両経路は同一の alias 導出 helper を使用する
- **AND** 同じ入力 config から同じ nested alias 値が得られる

### Requirement: Contrastive loss interfaces must expose runtime-required arguments only

Contrastive loss implementations MUST expose only runtime-used inputs in public call signatures. Implementations MUST NOT accept placeholder arguments that are ignored for implementation convenience.

#### Scenario: MXCLR aggregation call passes only required label statistics

- **WHEN** 開発者または coding agent が `MXCLR.score_graph` で agg を呼び出す
- **THEN** agg 呼び出しには当該 agg が要求する label statistics のみが渡される
- **AND** 未使用統計のダミー引数（受け取り後に破棄する引数）は公開契約に含まれない

#### Scenario: MSC forward accepts only the prototype context used in runtime

- **WHEN** 開発者または coding agent が `ContrastiveLitModule` の標準経路で MSC を実行する
- **THEN** MSC の公開 forward 契約は `z`, `labels`, `prototype` の runtime 入力に限定される
- **AND** queue/key 系の未使用引数は公開契約に含まれない

### Requirement: Contrastive loss configuration must expose explicit runtime arguments

Contrastive loss configurations MUST declare every runtime initialization argument in Hydra config so reproducibility review does not require reading Python defaults. Supported contrastive loss configs MUST exclude removed MCACR, MCACRWONEG, multi-scale MXCLR, and MXCLR Kendall choices. NPMI-aware MXCLR agg configurations MUST expose only the runtime initialization arguments accepted by their aggregation implementations.

#### Scenario: Resolve contrastive loss configs without hidden defaults

- **WHEN** 開発者または coding agent が `configs/contrastive/model/*.yaml` を使って loss を解決する
- **THEN** each supported loss config contains every runtime initialization argument for its implementation
- **AND** `configs/contrastive/model/mxclr.yaml` exposes `data_dir`, `instance_temperature`, `graph_temperature`, `dataset_name`, `sbert_model_name`, `sbert_max_length`, `whitening`, and `agg`
- **AND** `configs/contrastive/model/mxclr_rank.yaml` exposes `data_dir`, `instance_temperature`, `graph_temperature`, `rank_temperature`, `lambda_rank`, `dataset_name`, `sbert_model_name`, `sbert_max_length`, `whitening`, and `agg`
- **AND** NPMI-aware MXCLR agg configs do not expose removed Yule's Q beta arguments
- **AND** MCACR, MCACRWONEG, multi-scale MXCLR, and MXCLR Kendall configs are not supported choices

### Requirement: MXCLR label embeddings must support optional whitening

MXCLR label embedding construction MUST optionally apply whitening after the existing SentenceTransformer encoding path. The option MUST be disabled by default.

#### Scenario: Default label embedding construction is unchanged

- **WHEN** 開発者が `MXCLR(..., whitening=False)` または既定引数で初期化する
- **THEN** label embeddings are produced by the existing SentenceTransformer encoder call
- **AND** no whitening transform is applied

#### Scenario: Whitening transforms encoded label embeddings

- **WHEN** 開発者が `MXCLR(..., whitening=True)` を初期化する
- **THEN** MXCLR applies whitening to the encoded label embedding matrix
- **AND** the implementation does not add an AutoModel or AutoTokenizer pooling path
- **AND** the implementation does not add a separate whitening epsilon config

### Requirement: MXCLR rank loss must support ListMLE ranking with a single lambda coefficient

The repository MUST provide `MXCLRRank` as the ListMLE rank variant. The loss MUST reuse MXCLR agg-based sample-graph builders, MUST use a single non-negative coefficient `lambda_rank`, and MUST NOT hide additional batch-size normalization inside that coefficient.

#### Scenario: Instantiate MXCLR rank config with reusable agg group

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr_rank` を compose して instantiate する
- **THEN** `mxclr_rank` の `contrastive.model.loss_fn._target_` は `src.models.loss.mxclr_rank.MXCLRRank` として解決される
- **AND** `contrastive.model.loss_fn.agg` は `contrastive/model/agg@contrastive.model.loss_fn=<agg>` override で差し替えられる
- **AND** `mxclr_rank` は `rank_temperature` を明示 config key として解決する
- **AND** `BERTScore_F1` `BERTScore_F1_Uniform` `BERTScore_Precision` `BERTScore_Recall` を含む既存 MXCLR agg config をそのまま使用できる

#### Scenario: Compose uniform F1 MXCLR rank hparams search

- **WHEN** 開発者または coding agent が `hparams_search=mxclr_rank_bertscore_uniform_f1` を compose する
- **THEN** sweep params は `contrastive/model=mxclr_rank` を選択する
- **AND** `contrastive/model/agg@contrastive.model.loss_fn=BERTScore_F1_Uniform` を選択する
- **AND** `lambda_rank` は正値として設定される

#### Scenario: Combine MXCLR and ListMLE with explicit lambda rank

- **WHEN** 開発者または coding agent が `MXCLRRank.forward(z, labels)` または `MXCLRRank.forward(z, g_soft)` を実行する
- **THEN** 総損失は `MXCLR` の soft-target loss と row-wise ListMLE ranking loss の和として計算される
- **AND** ranking 項の寄与は `lambda_rank * listmle_loss` で制御される
- **AND** MXCLR soft-target loss は `instance_temperature` を使う
- **AND** ListMLE ranking 項の student scores は `rank_temperature` で scaling される
- **AND** 実装は ranking 項を batch size で追加正規化しない
- **AND** self-pair の対角成分は ranking 項から除外される
- **AND** `MXCLRRank` は removed Kendall-specific smoothness arguments を公開引数に持たない
- **AND** `rank_temperature` が 0 以下の場合は初期化時にエラーになる

### Requirement: Contrastive temperature parameters must use canonical naming

Contrastive loss implementations and configs MUST use `temperature`-based names for public temperature parameters instead of mixed aliases such as `temp` or `tau`.

#### Scenario: Resolve single-temperature losses with canonical key

- **WHEN** 開発者が Base、MulSupCon、MSC の config を解決する
- **THEN** 公開温度キーは `temperature` である
- **AND** `temp` や `tau` は公開 config key として使われない

#### Scenario: Resolve multi-temperature losses with role-specific keys

- **WHEN** 開発者が MXCLR, MXCLRRank, or t-MXCLR config を解決する
- **THEN** multiple temperatures are exposed with role-specific `temperature` names such as `instance_temperature`, `graph_temperature`, and `rank_temperature`
- **AND** removed MCACR/MCACRWONEG temperature keys are not retained through compatibility layers

#### Scenario: Validate canonical temperature keys across all supported losses

- **WHEN** 開発者または coding agent が `configs/contrastive/model/*.yaml` を対象に温度キー検証テストを実行する
- **THEN** 各 loss config の温度関連キーは対応する loss 実装の runtime 初期化引数と一致する
- **AND** 旧キー（`temp`, `tau`, `tau_s`, `temp_attract`, `temp_repulse`）はどのサポート loss でも公開 config key として現れない

### Requirement: Tokenized training encoder max length must default to 512

Tokenized datamodule settings for contrastive and classification training MUST default to `max_length=512`, and runtime datamodule constructor defaults MUST remain consistent with resolved config defaults.

#### Scenario: Resolve train config with 512 max length defaults

- **WHEN** 開発者が `uv run python src/train.py --cfg job --resolve` を実行する
- **THEN** `contrastive.data.max_length` は `512` として解決される
- **AND** `classification.data.max_length` は `512` として解決される

#### Scenario: Datamodule constructor defaults match config defaults

- **WHEN** 開発者または coding agent が datamodule を config 経由または既定引数で初期化する
- **THEN** `ClassificationDataModule` と `ContrastiveDataModule` の `max_length` 既定値は `512` である
- **AND** config とクラス既定値の不一致により解釈差が発生しない

### Requirement: Contrastive W&B epoch metrics must use a single explicit axis mapping

Contrastive epoch-aggregated loss metrics logged to W&B MUST use a single explicit `contrastive/epoch` axis mapping that does not conflict with the logger's default wildcard metric definition. The implementation MUST avoid wildcard stage mappings that also match the same metric names as the default `* -> trainer/global_step` definition.

#### Scenario: Map contrastive loss metrics to the epoch axis without wildcard overlap

- **WHEN** 開発者または coding agent が contrastive stage を W&B logger 付きで実行する
- **THEN** `contrastive/train/loss` と `contrastive/val/loss` は `contrastive/epoch` を step metric とする明示定義だけを持つ
- **AND** それらの metric は stage wildcard 定義と logger 既定 wildcard 定義の両方に同時一致しない

#### Scenario: Keep the epoch axis itself available

- **WHEN** 開発者または coding agent が contrastive stage の epoch 集約 metric を記録する
- **THEN** `contrastive/epoch` 自体は W&B 上で定義される
- **AND** `contrastive/train/loss` と `contrastive/val/loss` はその epoch 値に対して比較できる

### Requirement: Linear probe learning-rate sweep grid for contrastive epoch search

`configs/hparams_search/contrastive_epoch.yaml` MUST define the linear_probe learning-rate sweep grid with exactly two candidates for each stage: contrastive `5e-5,1e-4` and classification `1e-3,5e-4`. The same sweep config MUST resolve the MXCLR preset with `contrastive/model: mxclr`, `contrastive/model/agg@contrastive.model.loss_fn: BERTScore_F1`, and `contrastive.model.loss_fn.agg.transport_lambda: 5e-1`.

#### Scenario: Resolve contrastive and classification lr candidates from sweep config

- **WHEN** 開発者が `uv run python src/train.py hparams_search=contrastive_epoch --cfg hydra -p hydra.sweeper.params --resolve` を実行する
- **THEN** `contrastive.model.optimizer.lr` は `5e-5,1e-4` を候補として解決される
- **AND** `classification.model.optimizer.lr` は `1e-3,5e-4` を候補として解決される

#### Scenario: Resolve MXCLR preset from sweep config

- **WHEN** 開発者が `uv run python src/train.py hparams_search=contrastive_epoch --cfg hydra -p hydra.sweeper.params --resolve` を実行する
- **THEN** `contrastive/model` は `mxclr` として解決される
- **AND** `contrastive/model/agg@contrastive.model.loss_fn` は `BERTScore_F1` として解決される
- **AND** `contrastive.model.loss_fn.agg.transport_lambda` は `5e-1` として解決される

#### Scenario: Keep scientific notation in learning-rate grid

- **WHEN** 開発者または coding agent が当該 sweep 設定を更新する
- **THEN** learning rate は指数表記（例: `1e-3`）で記述される
- **AND** 小数表記（例: `0.001`）は使用しない

#### Scenario: Keep descending order in multi-value learning-rate candidates

- **WHEN** 開発者または coding agent が learning-rate 候補を複数値で列挙する
- **THEN** 候補は数値の降順（高い値から低い値）で記述される
- **AND** 例として `1e-4,5e-5` の順序を使用する

### Requirement: Canonical lr grids for post-contrastive linear_probe and finetune

For reproducible comparison planning, the canonical two-candidate learning-rate grids SHALL be fixed as follows.

#### Scenario: Canonical grid for contrastive -> linear_probe

- **WHEN** 開発者が contrastive 学習後に `classification/strategy@classification.model=linear_probe` で比較実験を計画する
- **THEN** `contrastive.model.optimizer.lr` は `1e-4,5e-5` を候補として使用する
- **AND** `classification.model.optimizer.lr` は `1e-3,5e-4` を候補として使用する

#### Scenario: Canonical grid for finetune

- **WHEN** 開発者が `classification/strategy@classification.model=finetune` で比較実験を計画する
- **THEN** `classification.model.optimizer.lr` は `1e-4,5e-5` を候補として使用する
- **AND** 候補数は 2 点を維持する

#### Scenario: Search-only config may temporarily pin single lr

- **WHEN** `configs/hparams_search/contrastive_epoch.yaml` のような探索専用 config を検証目的で一時運用する
- **THEN** 単一 LR 固定は許容される
- **AND** その固定値は恒久仕様変更を意味しない

### Requirement: Debug callback disabling must apply safely to classification stage

When a debug configuration disables global callbacks, the classification stage MUST also resolve without stage-local callback interpolation failures.

#### Scenario: debug=fdr resolves classification callbacks to null

- **WHEN** 開発者または coding agent が `uv run python src/train.py --config-name test --cfg job --resolve debug=fdr` を実行する
- **THEN** `classification.callbacks` は `null` として解決される
- **AND** `${callbacks.model_checkpoint}` のような global callback 参照解決で失敗しない

#### Scenario: debug=fdr completes both stages without callback interpolation failure

- **WHEN** 開発者または coding agent が Python 3.12 + GPU 環境で `uv run python src/train.py --config-name test debug=fdr` を実行する
- **THEN** contrastive stage は fast_dev_run で完了する
- **AND** classification stage も callback 補間エラーなく train/test を開始して完了できる

### Requirement: contrastive_epoch hparams config is search-only

`configs/hparams_search/contrastive_epoch.yaml` MUST be treated as a parameter-search-only configuration and MUST NOT be used as the canonical final-evaluation setting.

#### Scenario: Use contrastive_epoch for exploration only

- **WHEN** 開発者が `configs/hparams_search/contrastive_epoch.yaml` を参照して実験を計画する
- **THEN** 当該設定は探索段階（hparams search）専用として扱う
- **AND** 論文報告の最終 3-seed 評価設定は別設定で管理する

### Requirement: MXCLR agg configs resolve documented family defaults

MXCLR configuration MUST keep common scalar hyperparameters in `configs/contrastive/model/mxclr.yaml`. Agg-family-specific settings MUST live under `configs/contrastive/model/agg/` and MUST be selected through Hydra defaults rather than a Python-side registry. Each agg config MUST instantiate a concrete graph implementation directly from `src/models/loss/agg/`, and MXCLR runtime code MUST NOT keep those concrete implementations in the top-level loss module. The default MXCLR config MUST resolve label descriptions from `data_dir` and `dataset_name` without exposing a separate `label_description_path` config key.

#### Scenario: Resolve MXCLR default from agg config group

- **WHEN** 開発者が `PROJECT_ROOT=$(pwd) UV_CACHE_DIR=$PWD/tmp/uv-cache uv run python src/train.py --cfg job --resolve contrastive/model=mxclr` を実行する
- **THEN** `contrastive.model.loss_fn.agg._target_` は `src.models.loss.agg.bertscore_f1.BERTScoreF1Graph` として解決される
- **AND** `contrastive.model.loss_fn.data_dir` は `${contrastive.data.data_dir}` から解決される
- **AND** `contrastive.model.loss_fn.dataset_name` は `${contrastive.data.dataset_name}` から解決される
- **AND** `contrastive.model.loss_fn.sbert_model_name` は `sentence-transformers/all-roberta-large-v1` として解決される
- **AND** `contrastive.model.loss_fn.label_description_path` は解決対象に含まれない
- **AND** `contrastive.model.loss_fn.graph_builder` は解決対象に含まれない
- **AND** `src/models/loss/mxclr.py` は concrete agg 実装 class を持たない

### Requirement: MXCLR transport backend uses Python Optimal Transport
MXCLR transport distance computation MUST use Python Optimal Transport as the solver backend while preserving repository-owned cost and mass construction.

#### Scenario: Resolve balanced transport via Python Optimal Transport

- **WHEN** 開発者または coding agent が balanced transport path を実行する
- **THEN** balanced solver は `ot.sinkhorn2` を使用する
- **AND** exact solver path は利用されない

### Requirement: MXCLR transport helper contract must define shared inputs and outputs

The public helper in `src/models/loss/components/transport.py` MUST expose one canonical module contract: it accepts `labels_bin: [N, L]`, `cost_matrix: [L, L]`, `label_weights: [L]`, and an explicit transport strategy selector, and it returns a pairwise distance matrix `[N, N]`. Public helper names MUST NOT be split by transport family when the input/output contract is otherwise identical. The helper MUST NOT expose an extra backend-selection argument when the backend is fixed by implementation policy.

#### Scenario: Call shared transport helper for balanced families

- **WHEN** 開発者または coding agent が WMD または WRD の距離計算を呼び出す
- **THEN** 呼び出しは 1 つの公開 transport helper に strategy 指定で集約される
- **AND** WMD は active label frequency mass、WRD は active embedding-norm mass を使う

#### Scenario: Call shared transport helper for unbalanced family

- **WHEN** 開発者または coding agent が UOT の距離計算を呼び出す
- **THEN** 呼び出しは同じ公開 transport helper を使い strategy で unbalanced solver を選択する
- **AND** UOT は active embedding-norm mass を未正規化のまま使う

#### Scenario: Transport private helpers keep concise solver-oriented names

- **WHEN** 開発者または coding agent が transport module の private solver helper を更新する
- **THEN** private helper 名は `transport` のような module context を重複させない
- **AND** sinkhorn / unbalanced sinkhorn の solver 差分だけを表す

### Requirement: Label statistics helpers must use concise canonical names

The public helpers in `src/models/loss/components/label_stats.py` MUST expose concise canonical names based on their documented module contracts. train.csv-derived label statistics MUST NOT remain duplicated in top-level loss modules. Shared aggregation helper modules for MXCLR MUST NOT exist when each agg implementation owns different concrete logic.

#### Scenario: Compute label statistics from the shared train.csv contract

- **WHEN** 開発者または coding agent が label statistics helper を呼び出す
- **THEN** canonical helper 名は `compute_frequency` `compute_idf` `compute_npmi` である
- **AND** `label_stats` module contract が label counts / pair counts / train.csv source を定義する
- **AND** top-level loss modules do not duplicate train.csv-derived statistics that belong in shared helpers

#### Scenario: Keep MXCLR aggregation logic in concrete agg modules

- **WHEN** 開発者または coding agent が MXCLR agg 実装を更新する
- **THEN** concrete agg logic は `src/models/loss/agg/*.py` の各 module 内で完結する
- **AND** `src/models/loss/components/aggregation.py` は存在しない

### Requirement: MXCLR must auto-load agg-required label statistics

MXCLR MUST inspect the selected agg implementation and auto-load any required train.csv-derived label statistics during initialization. Concrete agg modules MUST declare which of `npmi`, `label_idf`, and `label_frequency` they require, and `src/models/loss/mxclr.py` MUST consume that declaration without keeping a concrete-agg registry.

### Requirement: MXCLR supports BERTScore F1 aggregation

MXCLR MUST support the agg choice `BERTScore_F1`. `BERTScore_F1` MUST use the label similarity matrix and IDF weighting contract, treat the forward directional score as Precision, the reverse directional score as Recall, and return their harmonic mean `2PR / (P + R)` as the pairwise score.

#### Scenario: Build MXCLR score graph with BERTScore F1

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr contrastive/model/agg@contrastive.model.loss_fn=BERTScore_F1` を compose して `score_graph(labels)` を呼び出す
- **THEN** 実装は `npmi` と `label_idf` を自動初期化して agg へ渡す
- **AND** 出力 score graph は有限値で対称かつ `[0, 1]` 範囲に収まる

#### Scenario: Harmonic-mean aggregation combines directional scores

- **WHEN** 開発者または coding agent が同じ labels と label similarity matrix に対して `BERTScore_Precision` `BERTScore_Recall` `BERTScore_F1` を比較する
- **THEN** `BERTScore_F1` は同じ方向別 score を使って `2PR / (P + R)` を返す

### Requirement: MXCLR supports uniform-weight BERTScore F1 aggregation

MXCLR MUST support the agg choice `BERTScore_F1_Uniform`. `BERTScore_F1_Uniform` MUST use the same label similarity matrix construction and harmonic mean as `BERTScore_F1`, but MUST weight every active source label equally instead of using IDF weights.

#### Scenario: Build MXCLR score graph with uniform BERTScore F1

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr_rank contrastive/model/agg@contrastive.model.loss_fn=BERTScore_F1_Uniform` を compose して `score_graph(labels)` を呼び出す
- **THEN** 実装は `npmi` を自動初期化して agg へ渡す
- **AND** `label_idf` は agg が要求する統計に含まれない
- **AND** 出力 score graph は有限値で対称かつ `[0, 1]` 範囲に収まる

#### Scenario: Uniform BERTScore F1 differs from IDF-weighted BERTScore F1

- **WHEN** 同じ labels, label embeddings, and npmi に対して `BERTScore_F1` and `BERTScore_F1_Uniform` を比較する
- **THEN** `BERTScore_F1` は source label weights として `label_idf` を使用する
- **AND** `BERTScore_F1_Uniform` は active source labels を等重みで平均する

### Requirement: W&B logs canonical agg alias for BERTScore F1

When training logs MXCLR hyperparameters to W&B, the derived comparison alias `contrastive.model.loss_fn.agg_name` MUST preserve the canonical names `BERTScore_F1` and `BERTScore_F1_Uniform` for the F1 aggs.

#### Scenario: Derive canonical agg alias from BERTScore target

- **WHEN** 開発者または coding agent が `_target_=src.models.loss.agg.bertscore_f1.BERTScoreF1Graph` を含む config を W&B alias 導出へ渡す
- **THEN** `contrastive.model.loss_fn.agg_name` は `BERTScore_F1` として記録される
- **AND** `loss_fn.agg` subtree は上書きされない

#### Scenario: Derive canonical agg alias from uniform BERTScore F1 target

- **WHEN** 開発者または coding agent が `_target_=src.models.loss.agg.bertscore_f1.BERTScoreUniformF1Graph` を含む config を W&B alias 導出へ渡す
- **THEN** `contrastive.model.loss_fn.agg_name` は `BERTScore_F1_Uniform` として記録される
- **AND** `loss_fn.agg` subtree は上書きされない

### Requirement: MXCLR supports BERTScore Precision and Recall aggregation

MXCLR MUST support new agg choices `BERTScore_Precision` and `BERTScore_Recall` in addition to existing agg implementations. Both aggs MUST reuse the same label similarity matrix and IDF weighting contract as `BERTScore_F1`. `BERTScore_Precision` MUST return the forward directional score from source label set to target label set, and `BERTScore_Recall` MUST return the reverse directional score for the same pair.

#### Scenario: Build MXCLR score graph with BERTScore Precision

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr contrastive/model/agg@contrastive.model.loss_fn=BERTScore_Precision` を compose して `score_graph(labels)` を呼び出す
- **THEN** 実装は `npmi` と `label_idf` を自動初期化して agg へ渡す
- **AND** 出力 score graph は有限値かつ `[0, 1]` 範囲に収まる

#### Scenario: Build MXCLR score graph with BERTScore Recall

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr contrastive/model/agg@contrastive.model.loss_fn=BERTScore_Recall` を compose して `score_graph(labels)` を呼び出す
- **THEN** 実装は `npmi` と `label_idf` を自動初期化して agg へ渡す
- **AND** 出力 score graph は有限値かつ `[0, 1]` 範囲に収まる

#### Scenario: Precision and Recall remain directional counterparts

- **WHEN** 開発者または coding agent が同じ labels と label similarity matrix に対して `BERTScore_Precision` と `BERTScore_Recall` を計算する
- **THEN** `BERTScore_Recall(i, j)` は `BERTScore_Precision(j, i)` と一致する
- **AND** `BERTScore_F1(i, j)` は同じ pair の Precision/Recall から `2PR / (P + R)` を計算する

### Requirement: W&B logs canonical agg aliases for BERTScore Precision and Recall

When training logs MXCLR hyperparameters to W&B, the derived comparison alias `contrastive.model.loss_fn.agg_name` MUST preserve the canonical names `BERTScore_Precision` and `BERTScore_Recall` for the new aggs.

#### Scenario: Derive canonical agg alias from BERTScore Precision target

- **WHEN** 開発者または coding agent が `_target_=src.models.loss.agg.bertscore_f1.BERTScorePrecisionGraph` を含む config を W&B alias 導出へ渡す
- **THEN** `contrastive.model.loss_fn.agg_name` は `BERTScore_Precision` として記録される
- **AND** `loss_fn.agg` subtree は上書きされない

#### Scenario: Derive canonical agg alias from BERTScore Recall target

- **WHEN** 開発者または coding agent が `_target_=src.models.loss.agg.bertscore_f1.BERTScoreRecallGraph` を含む config を W&B alias 導出へ渡す
- **THEN** `contrastive.model.loss_fn.agg_name` は `BERTScore_Recall` として記録される
- **AND** `loss_fn.agg` subtree は上書きされない

### Requirement: Training internals must use canonical inline normalization

Training-related modules MUST implement row-wise L2 normalization by calling `torch.nn.functional.normalize` directly. For contrastive loss execution, normalization ownership MUST live in each contrastive loss implementation, and the training module MUST NOT require caller-side pre-normalization of `z`.

#### Scenario: Normalize contrastive embeddings and prototypes inline

- **WHEN** 開発者または coding agent が contrastive module や contrastive loss 実装を更新する
- **THEN** 行方向 L2 正規化は torch.nn.functional.normalize を直接呼び出して実装される
- **AND** normalize_embeddings や _normalize_prototype のような単純 wrapper は残さない
- **AND** `Base` `MulSupCon` `MXCLR` `MXCLRRank` `MSC` は loss 計算時に `z` を内部で正規化する
- **AND** `ContrastiveLitModule` は loss 呼び出しに必要な `z` 正規化を事前条件として持たない

### Requirement: Classification datamodule must share one dataset requirement helper

Classification datamodule MUST validate train/val/test `TokenizedDataset` existence through one helper that accepts a split name. The implementation MUST NOT keep duplicated per-split requirement helpers.

#### Scenario: Resolve split datasets through one shared helper

- **WHEN** 開発者または coding agent が classification datamodule の dataloader 実装を更新する
- **THEN** train_dataloader、val_dataloader、test_dataloader は共通の dataset requirement helper を使って対象 split を取得する
- **AND** split ごとに同型の _require_data_train、_require_data_val、_require_data_test を個別実装しない

### Requirement: Config numeric literals use scientific notation except epoch and batch-size counters

When updating numeric literals in config files, developers MUST use scientific notation for fractional hyperparameters (for example, `1e-2`) and MUST keep `epoch`/`batch_size` counters in plain integer notation (for example, `80`, `64`).

#### Scenario: Use mixed notation by numeric role

- **WHEN** 開発者または coding agent が `configs/` 配下の設定ファイル内で数値を追加・更新する
- **THEN** 学習率や比率などの小数ハイパーパラメータは `1e-2` のように指数表記で記述される
- **AND** `min_epochs` `max_epochs` `check_val_every_n_epoch` `batch_size` は `80` `64` のような整数表記を使用する

### Requirement: Seed initialization must honor explicit zero values

Training entrypoint MUST execute random seed initialization whenever `seed` is explicitly set, including `seed=0`.

#### Scenario: Seed initialization runs when seed is zero

- **WHEN** 設定上 `seed=0` が明示されている
- **THEN** 学習開始時に `lightning.seed_everything(0, workers=True)` が実行される

#### Scenario: Seed initialization is skipped only when seed is unset

- **WHEN** 設定上 `seed` が未設定または `None` である
- **THEN** 学習開始時の seed 初期化は実行されない

### Requirement: Default runtime acceleration settings

Training defaults MUST enable runtime acceleration features that are already supported by the repository implementation.

#### Scenario: Resolve default compile settings for both stages

- **WHEN** 開発者が `PROJECT_ROOT=$(pwd) uv run python src/train.py --cfg job --resolve` を実行する
- **THEN** `contrastive.model.compile` は `true` として解決される
- **AND** `classification.model.compile` は `true` として解決される

#### Scenario: Resolve default pinned-memory dataloaders for tokenized stages

- **WHEN** 開発者が `PROJECT_ROOT=$(pwd) uv run python src/train.py --cfg job --resolve` を実行する
- **THEN** `contrastive.data.pin_memory` は `true` として解決される
- **AND** `classification.data.pin_memory` は `true` として解決される

#### Scenario: Seed initialization runs with zero

- **WHEN** 開発者が `uv run python src/train.py seed=0` を実行する
- **THEN** 実装は `lightning.seed_everything(0, workers=True)` を呼び出す

#### Scenario: Seed initialization is skipped only when seed is unset

- **WHEN** 設定上 `seed` が未設定または `None` である
- **THEN** 学習開始時の seed 初期化は実行されない

### Requirement: Tokenized sampler refresh for GCBS and DPP

When contrastive sampler refresh recomputes embeddings for GCBS or DPP, the system MUST use tokenized tensor batches and MUST NOT require raw text reconstruction inside the refresh loop.

#### Scenario: GCBS refresh uses tokenized tensors

- **WHEN** sampler_type が `gcbs` で epoch refresh が実行される
- **THEN** 埋め込み再計算は `input_ids` と `attention_mask` のバッチ入力で行われる
- **AND** refresh 中に raw text の再トークナイズを要求しない

#### Scenario: DPP refresh uses tokenized tensors

- **WHEN** sampler_type が `dpp` で epoch refresh が実行される
- **THEN** 埋め込み再計算は `input_ids` と `attention_mask` のバッチ入力で行われる
- **AND** 生成された埋め込みが DPP sampler 初期化へ渡される

### Requirement: Sampler tests must separate shared integration from targeted output hygiene

Sampler validation MUST check system-level sampler contracts through shared integration tests. Generic sampler switching and DataModule wiring MUST be checked in shared integration tests so sampler behavior is validated at the training-system boundary.

#### Scenario: Keep sampler switching in shared integration

- **WHEN** 開発者または coding agent が `shuffle`, `gcbs`, `dpp` の sampler 切替や初期化順序を検証する
- **THEN** 検証は shared integration test で行う
- **AND** sampler 共通の functional contract は 1 か所で回帰検知できる

### Requirement: Tokenized-only mini-batch execution path

Training modules MUST process tokenized tensor mini-batches only and MUST NOT keep raw-text fallback branches in runtime batch handling.

#### Scenario: Encoder forward expects tokenized tensors

- **WHEN** encoder forward が training module から呼ばれる
- **THEN** 入力契約は `input_ids` と `attention_mask` を含む tensor dict である
- **AND** encoder 内に raw text 再トークナイズ分岐を持たない

#### Scenario: Stage modules handle `(inputs, labels)` tuple

- **WHEN** classification または contrastive の train/val/test step が実行される
- **THEN** バッチ契約は `(tokenized_inputs, labels)` の2要素タプルである
- **AND** text payload の有無に応じた分岐を行わない

### Requirement: Empty-text zero override on classification test

Classification test evaluation MUST set prediction rows to zero for samples marked as empty text by preprocessing metadata.

#### Scenario: Empty text sample is zeroed in test prediction

- **WHEN** classification `test_step` が `empty_text_mask=True` を含むバッチを処理する
- **THEN** 対応する予測行は全ラベル 0 に上書きされる
- **AND** `empty_text_mask=False` の行は通常のしきい値予測を保持する

#### Scenario: Override uses tokenized metadata contract

- **WHEN** 空テキスト上書き判定が実行される
- **THEN** 判定は `inputs["empty_text_mask"]` のみを参照する
- **AND** raw text payload を runtime batch に含めない

### Requirement: Wandb run termination must reflect training outcome

Training wrapper MUST finalize wandb runs with an explicit exit code that matches the execution outcome. Successful runs MUST call `wandb.finish(exit_code=0)`, and failed runs MUST call `wandb.finish(exit_code!=0)`.

#### Scenario: Successful training marks wandb run as finished

- **WHEN** 学習処理が例外なく完了する
- **THEN** 実装は `wandb.finish(exit_code=0)` を呼び出す

#### Scenario: Failed training marks wandb run as failed

- **WHEN** 学習処理中に例外が発生する
- **THEN** 実装は `wandb.finish(exit_code=1)` を呼び出す
- **AND** 例外は再送出され、呼び出し元に失敗が伝播する

### Requirement: Atomic commit granularity for reproducible changes

Developers MUST keep each commit to a single logical change so that history remains traceable and reproducible.

#### Scenario: Split unrelated edits into separate commits

- **WHEN** 開発者が機能変更と無関係な整形またはリネームを同時に行った
- **THEN** それらは別 commit に分割される

#### Scenario: Keep commit-level validation

- **WHEN** 開発者が commit を作成する
- **THEN** その commit 単体で設定解決または該当 fast テストが成立する

### Requirement: Topic-scoped push granularity with pre-push checks

Developers MUST push only coherent topic commits and MUST satisfy pre-commit quality checks before pushing.

#### Scenario: Push coherent topic only

- **WHEN** 開発者がリモートへ push する
- **THEN** 同一トピック change に属する commit 群のみを push し、未整理の暫定 commit を含めない

#### Scenario: Run mandatory checks before push

- **WHEN** 開発者が PR/push 前最終確認を行う
- **THEN** `uv run pre-commit run -a` が成功している
- **AND** `uv run pytest -m "not slow"` は推奨だが必須ではない

### Requirement: Public class naming for contrastive loss implementations

The training specification MUST define the canonical public class names for built-in contrastive losses.

#### Scenario: Resolve canonical class names for built-in losses

- **WHEN** 開発者または coding agent が built-in contrastive loss 実装の公開名を確認する
- **THEN** canonical class names は `Base`, `MulSupCon`, `MXCLR`, `MXCLRRank`, `MSC` である
- **AND** loss 実装ファイル名は `src/models/loss/<loss_name>.py` 形式を維持する

# 学習仕様（Training Spec）

### Requirement: MXCLR default initialization must resolve dataset-scoped label descriptions

The default MXCLR configuration MUST initialize by reading `<data_dir>/<dataset_name>/label_descriptions.json`. MXCLR MUST NOT require a separate label-description path argument. If the dataset-scoped JSON is missing, MXCLR MUST fail eagerly before training starts.

#### Scenario: Instantiate MXCLR default config from tracked AAPD descriptions

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr` を compose して model を instantiate する
- **THEN** `data/aapd/label_descriptions.json` を用いて初期化に成功する

#### Scenario: Instantiate MXCLR with custom dataset descriptions

- **WHEN** 開発者または coding agent が `data_dir=<tmp_root>` `dataset_name=<custom_dataset>` かつ `<tmp_root>/<custom_dataset>/label_descriptions.json` を用意して MXCLR を初期化する
- **THEN** MXCLR は dataset 名に依存した追加制約なしで初期化に成功する

#### Scenario: Missing dataset-scoped descriptions fail eagerly

- **WHEN** 開発者または coding agent が `<data_dir>/<dataset_name>/label_descriptions.json` が存在しない状態で MXCLR を初期化する
- **THEN** MXCLR は学習開始前に FileNotFoundError を送出する

## 0. 前提（環境と実行）

- 実行は必ず uv 仮想環境を使用する（`.venv/bin/python3`）。
- 実行は必ず `uv run ...` 経由で行う。

### PROJECT_ROOT（必須）

- `configs/paths/default.yaml` で `root_dir: ${oc.env:PROJECT_ROOT}` を使用している。
- つまり環境変数 `PROJECT_ROOT` が未設定だとパス解決に失敗する。

推奨：

- リポジトリ直下で `export PROJECT_ROOT=$(pwd)` を設定してから実行する。

## 1. エントリポイントと設定合成

- エントリポイント：`src/train.py`
- Hydra 起点：
  - `@hydra.main(version_base="1.3", config_path="../configs", config_name="train.yaml")`
  - つまり `configs/train.yaml` を起点に設定が合成される。

## 2. train.yaml の defaults（デフォルトで実行されるステージ）

`configs/train.yaml` の defaults は以下（確定）：

- `contrastive: train`
- `classification: train`
- `hydra: default`

→ デフォルトでは contrastive と classification の設定を読み込む。

## 3. ステージ実行ロジック（src/train.py の実装で確定）

各ステージ（例：contrastive / classification）は `stage_cfg` に基づき以下を行う：

### 3.1 インスタンス化

- `datamodule = hydra.utils.instantiate(stage_cfg.data)`
- `model = hydra.utils.instantiate(stage_cfg.model)`
- `trainer_cfg` を合成し、`trainer = hydra.utils.instantiate(trainer_cfg, callbacks=callbacks, logger=logger)` を生成する。

### 3.2 ハイパーパラメータのログ

- logger が存在する場合、`log_hyperparameters(object_dict)` を呼ぶ。

### 3.3 学習（fit）の条件と ckpt_path

- 条件：`if stage_cfg.get("train", True):`
  - `train` が未指定なら True 扱い。
- 実行：
  - `trainer.fit(model=model, datamodule=datamodule, ckpt_path=stage_cfg.get("ckpt_path"))`
- `ckpt_path` はステージ設定に `ckpt_path` があればそれを使用し、なければ None（=通常の新規学習）。

### 3.4 評価（test）の条件と ckpt 選択

- 条件：`if stage_cfg.get("test", False):`

  - `test` が未指定なら False 扱い。

- 実行前に `ckpt_path` を以下で決める（確定）：

  1. `ckpt_path = None`
  2. `ckpt_cb = getattr(trainer, "checkpoint_callback", None)`
  3. `ckpt_cb` が存在すれば `ckpt_cb.best_model_path` を優先して `ckpt_path` に入れる
  4. best が見つからない場合は警告を出し、`ckpt_path=None` のまま test を実行
     - この場合は「現在の重み（current weights）」で test する。

- test 実行（確定）：

  - `trainer.test(model=model, datamodule=datamodule, ckpt_path=ckpt_path)`
  - 直後に `Best ckpt path: {ckpt_path}` をログ出力する。

### 3.5 test 後の ckpt 削除（重要：挙動として仕様化）

test 実行後、以下のファイル削除を試みる（確定）：

- `ckpt_path`（best ckpt があれば）
- `last.ckpt`（`ckpt_cb.dirpath/last.ckpt` が組める場合）
  存在しなければ警告、削除に失敗しても警告で続行。

## 4. ステージ設定キー（仕様として固定）

各ステージの挙動を決めるキーは以下（実装から確定）：

- `train`（default True）
- `test`（default False）
- `ckpt_path`（fit の再開用。未指定なら None）

## 5. パス仕様（configs/paths/default.yaml で確定）

- `root_dir = ${oc.env:PROJECT_ROOT}`
- `data_dir = ${paths.root_dir}/data/`
- `log_dir  = ${paths.root_dir}/logs/`
- `output_dir = ${hydra:runtime.output_dir}`（Hydra が動的に作成）
- `work_dir = ${hydra:runtime.cwd}`

※ `output_dir` の生成パターンは `configs/hydra/default.yaml` で定義される。

## 6. wandb 仕様（configs/logger/wandb.yaml で確定）

- logger 実体：`lightning.pytorch.loggers.wandb.WandbLogger`
- `project: "multi-label-supcon"`
- `save_dir: ${paths.output_dir}`
- `group: ""`（デフォルト空、必要なら override）
- `tags: []`（デフォルト空、必要なら override）
- `offline: False`
- `log_model: False`（Lightning ckpt の自動アップロードなし）

補足（コードの挙動として確定）：

- ckpt が wandb run directory にコピーされるのを抑止する処理がある（`_ignore_wandb_ckpt_artifacts()`）。

## 7. contrastive → classification への “事前学習 encoder” 引き渡し（実装で確定）

`src/train.py` は contrastive 学習後に、classification の encoder 初期化へ ckpt パスを渡す処理を持つ（確定）：

- まず `checkpoint_callback.best_model_path` があればそれを `pretrain_ckpt_path` にする。
- best が無い場合、`contrastive_cfg.get("save_last_encoder", True)` が True なら
  `contrastive_last.ckpt` を保存して `pretrain_ckpt_path` にする（`torch.save({"state_dict": model.state_dict()}, pretrain_ckpt_path)`）。
- classification 側に `pretrained_encoder_path` が未指定なら、
  `classification_cfg.model.pretrained_encoder_path = pretrain_ckpt_path` を設定する。
- `contrastive_last.ckpt` を作った場合は、後で削除を試みる（存在しなければ警告）。

## 8. 実行例（実際に成り立つ形）

前提：

- `export PROJECT_ROOT=$(pwd)`

例：

- logger を wandb にする：

  - `uv run python src/train.py logger=wandb`

- seed を固定：

  - `uv run python src/train.py seed=0 logger=wandb`

- contrastive の sampler を指定（存在が help で確認できる）：

  - `uv run python src/train.py contrastive/sampler=gcbs logger=wandb`

- 合成後の設定を確認（推奨）：

  - `uv run python src/train.py --cfg job --resolve`

## 9. hparams_search 運用ルール（GCBS quantile）

- GCBS の quantile 探索は `configs/hparams_search/test1.yaml` から `configs/hparams_search/test4.yaml` に内包して管理する。
- `configs/hparams_search/gcbs_quantile_grid.yaml` は運用対象外（廃止）とする。
- 対象ファイルでは以下を明示する：
  - `contrastive/sampler@contrastive.data: gcbs`
  - `contrastive.data.gcbs.quantile: 0.99, 0.98, 0.97`
  - `contrastive.data.gcbs.chunk_size: 10`

## 10. Contrastive loss 実装の命名

- contrastive loss 実装は可読性のため簡潔で一貫した命名を使用する。
- loss 実装ファイル名は `src/models/loss/<loss_name>.py` の形式に統一し、`loss_` などの冗長な接頭辞を付けない。
- base loss の公開クラス名は `Base` とする。
- supcon loss の公開クラス名は `MulSupCon` とする。
- `MulSupCon` は batch 中の各正ラベルを個別 anchor row に展開し、そのラベルを持つ他サンプル集合に対する supervised contrastive objective を計算する。
- `MulSupCon` の最終 loss は、展開された label-wise rows の平均で集約する。
- MSC loss の公開クラス名として `MSC` を提供する。
- 共通集約契約: labels 集約は初期化引数 `agg`（`BERTScore_F1` / `BERTScore_F1_Uniform` / `BERTScore_Precision` / `BERTScore_Recall`）で切り替える。
- 共通集約契約（数値制約）: 出力は有限値とし、必要に応じて [0, 1] にクリップする。
- contrastive loss へ渡す埋め込みの L2 正規化は `src/models/contrastive_module.py` の `ContrastiveLitModule._project` で実施する。
- loss 実装側（例: `src/models/loss/mxclr.py`）は埋め込み正規化を重複実装しない。
- `configs/contrastive/model/base.yaml` の `loss_fn._target_` は `src.models.loss.base.Base` を参照する。
- `configs/contrastive/model/ml_supcon.yaml` の `loss_fn._target_` は `src.models.loss.ml_supcon.MulSupCon` を参照する。
- `configs/contrastive/model/mxclr.yaml` の `loss_fn._target_` は `src.models.loss.mxclr.MXCLR` を参照する。
- `configs/contrastive/model/mxclr_rank.yaml` の `loss_fn._target_` は `src.models.loss.mxclr_rank.MXCLRRank` を参照する。
- `configs/contrastive/model/msc.yaml` の `loss_fn._target_` は `src.models.loss.msc.MSC` を参照する。
- MXCLR は標準経路で `loss_fn(z, labels)` を受け取り、内部で `score_graph(labels)` を使って sample-pair score 行列へ変換する。
- MXCLR は `data_dir/<dataset_name>/label_descriptions.json` を読み込んで Sentence-BERT でラベル間意味類似度行列を常時構築する。
- MXCLR はラベル説明文エンコード長 `sbert_max_length` を明示設定で受け取り、初期化時に正値検証したうえで `SentenceTransformer.max_seq_length` へ適用する。
- MXCLR の `score_graph(labels)` は共通集約契約（`agg`）の出力をそのまま返す。
- MXCLR の loss 本体は batch 内候補 cross entropy をそのまま集計し、focal-style weighting 用の追加ハイパーパラメータを公開契約に含めない。
- MXCLR-family loss は agg-level regularizer hook を呼び出さず、labels 経路でも graph 直入力経路でも score graph 由来の contrastive objective のみを計算する。
- MXCLR は semantic 初期化設定が不正（説明ファイル不在、ラベル数不一致など）の場合、学習開始前に初期化例外を送出する。
- MSC は標準経路で `loss_fn(z, labels, prototype)` を受け取り、`ContrastiveLitModule` が保持する学習可能 prototype を正規化して明示供給する。prototype 未指定時は例外を送出する。
- `classification.py` を除く contrastive loss module は、`forward` を入力検証と orchestration に限定し、loss 本体計算は module-level private helper へ委譲する。
- loss 本体 helper の命名は `_compute_<loss>_loss` に統一する。
- `Base` `MSC` で共有する label overlap の OR-count / union-count は `src/models/loss/components/label_overlap.py` の shared helper を使い、top-level loss module ごとに重複実装しない。
- 単純な shape / config / column existence の guard は、pytest で独立に守る helper として切り出さず、主要関数の冒頭へ直接記述する。

#### Scenario: MulSupCon computes label-wise expanded supervised contrastive loss

- **WHEN** `MulSupCon.forward(z, labels)` が multi-label batch に対して呼ばれる
- **THEN** batch 中の各正ラベルは個別 anchor row に展開される
- **AND** 各 row は同じラベルを持つ他サンプルを positives として supervised contrastive loss を計算する
- **AND** 最終 loss は展開された label-wise rows を平均した有限スカラーになる

## 11. Contrastive 既定 model と fixed epoch

- `configs/contrastive/train.yaml` の defaults では `contrastive/model@model: base` を既定値とする。
- ml_supcon を使う場合は `contrastive/model=ml_supcon` を明示指定する。
- `configs/contrastive/train.yaml` の `contrastive.trainer.max_epochs` は 80 で固定する。
- `configs/hparams_search/contrastive_epoch.yaml` は再現実験用の固定設定として `contrastive.trainer.max_epochs: 80` を使用する。
- 同設定の `contrastive.model.optimizer.lr` は `5e-5,1e-4` を sweep 対象とする。
- 同設定の `classification.model.optimizer.lr` は `1e-3,5e-4` を sweep 対象とする。
- learning rate の記法は指数表記（例: `1e-3`, `1e-4`）を使用し、`0.001` や `0.0001` の小数表記は使用しない。

## 12. Loss 実装の pytest 要件

- `src/models/loss` 配下の contrastive loss 実装の単体検証は pytest を標準経路とする。
- `src/models/loss/<loss_file>.py` の `__main__` 自己テストは必須要件にしない。
- 各 loss 向け pytest は最低限、以下を検証する。
  - 正常入力で有限スカラーを返すこと。
  - 主要な入力不正または設定不正に対して想定例外を送出すること（少なくとも 1 ケース）。
- NPMI など一時ファイルが必要な pytest は `multi-label/tmp` 配下を使用し、終了時にクリーンアップする。
- 詳細な挙動検証は property test や config instantiate test と併用してよい。

## 13. テスト階層と実行規約

本リポジトリの検証は、以下の階層で運用する。

### 13.1 単体テスト（contrastive loss pytest）

- 対象: `tests/test_contrastive_losses.py` と関連 property test。
- 目的: Loss 単体の最小挙動、入力検証、Hydra instantiate、必要な一時ファイル処理を pytest で確認する。
- 実行例:
  - `uv run pytest tests/test_contrastive_losses.py -q`
  - `uv run pytest tests/test_property_based.py -k "base or mxclr or log_softmax"`

### 13.2 構成・コンポーネント統合テスト（pytest）

- 対象: `tests/test_configs.py`
- 目的: Hydra 設定の instantiate 可否を確認し、設定破損を早期検知する。
- 実行例: `uv run pytest tests/test_configs.py -q`

### 13.3 学習フロー統合テスト（pytest）

- 対象:
  - `tests/test_train_integration.py`
  - `tests/test_train_cpu_slow.py`
  - `tests/test_train_gpu.py`
  - `tests/test_train_gpu_slow.py`
- 目的: 学習ループ、resume、DDP sim、GPU fast-dev-run などの学習経路を marker 境界と一致する module 単位で確認する。
- resume 検証ルール:
  - checkpoint ファイル存在を検証する場合、対象 stage は checkpointing 有効であること。
  - train 系 module は stage の `test=true` 実行後に ckpt 削除を試行するため、artifact 存在を検証するケースでは対象 stage の `test=false` を明示すること。
- 実行例:
  - `uv run pytest tests/test_train_integration.py -q`
  - `uv run pytest tests/test_train_cpu_slow.py -q`
  - `uv run pytest tests/test_train_gpu.py -q`
  - `uv run pytest tests/test_train_gpu_slow.py -q`

### 13.4 評価フロー統合テスト（pytest）

- 対象: `tests/test_eval.py`
- 目的: train 後の checkpoint を使った eval 経路とメトリクス整合性を確認する。
- 実行例: `uv run pytest tests/test_eval.py -q`

### 13.5 Sweep 統合テスト（pytest + shell）

- 対象: `tests/test_sweeps.py`
- 目的: Hydra multirun/sweep の実行経路を確認する。
- 実行例: `uv run pytest tests/test_sweeps.py -q`

### 13.6 実機 GPU 統合実行（スクリプト）

- 対象: `scripts/test.sh`
- 目的: 実運用に近い条件で train エントリポイントを GPU で実行し、最低限の end-to-end 経路を確認する。
- 実行規約:
  - sandbox ではなくローカルマシンで実行する。
  - train エントリポイントは `uv run python src/train.py` で起動する。
  - `PROJECT_ROOT` 未設定時はスクリプト内でリポジトリルートを既定設定する。
  - 実行ログは `multi-label/tmp/test.log` を使用する。
- 実行例:
  - `bash scripts/test.sh`
  - もしくは uv 環境を強制する場合は `uv run bash scripts/test.sh`

### 13.7 データコンポーネント自己テスト（実装ファイル末尾）

- 対象:
  - `src/data/components/gcbs.py`
  - `src/data/components/dpp.py`
  - `src/data/components/classification_dataset.py`
  - `src/data/classification_datamodule.py`
  - `src/data/contrastive_datamodule.py`
- 目的:
  - sampler/permutation の不変条件を学習実行前に検証する。
  - CSV 契約（必須列、値型、異常系）の破損を早期検知する。
  - dataloader 構築と sampler 初期化経路の破損を早期検知する。
- 実行例:
  - `uv run python src/data/components/gcbs.py`
  - `uv run python src/data/components/dpp.py`
  - `uv run python src/data/components/classification_dataset.py`
  - `uv run python src/data/classification_datamodule.py`
  - `uv run python src/data/contrastive_datamodule.py`

### 13.8 モデル部品自己テスト（実装ファイル末尾）

- 対象:
  - `src/models/components/mlp_head.py`
- 目的:
  - projection head の入出力 shape 契約と異常入力を早期検知する。
- 実行例:
  - `uv run python src/models/components/mlp_head.py`

### 13.9 DataModule/sampler 統合テスト（pytest, integration）

- 対象:
  - `tests/test_data_integration.py`
- 目的:
  - `ClassificationDataModule` と `ContrastiveDataModule` の統合経路を tiny データで検証する。
  - `sampler_type=shuffle/gcbs/dpp` 切替と初期化順序エラーを pytest で回帰検知する。
- 実行例:
  - `uv run pytest tests/test_data_integration.py -q`
  - `uv run pytest -m integration tests/test_data_integration.py -q`

## 14. 新規 Loss 追加の標準手順（OpenSpec 運用）

新しい contrastive loss を追加する場合は、OpenSpec change を作成した上で以下を実施する。

### 14.1 config 追加手順（必須）

- `src/models/loss/<loss_file>.py` に loss クラスを実装する。
- `src/models/loss/__init__.py` の公開名に追加する。
- `configs/contrastive/model/<loss_name>.yaml` を追加し、`loss_fn._target_` を実装クラスへ設定する。
- 必要に応じて `configs/contrastive/model/default.yaml` または実験用オーバーライドから選択可能にする。

### 14.2 test 手順（必須）

- 1. Loss 単体 pytest:
  - `uv run pytest tests/test_contrastive_losses.py -q`
- 2. 設定解決テスト:
  - `uv run pytest tests/test_configs.py -q`
- 3. 学習・評価・sweep 統合テスト（変更影響に応じて実施）:
  - `uv run pytest tests/test_train_integration.py -q`
  - `uv run pytest tests/test_eval.py -q`
  - `uv run pytest tests/test_sweeps.py -q`
- 4. GPU 実機確認（必要時）:
  - `bash scripts/test.sh`

### 14.3 change tasks への記録（必須）

- 上記の各手順を change の `tasks.md` にチェックボックスとして定義する。
- 実施した項目は完了チェックし、未実施項目は理由を残す。
- レビュー時に、tasks と実行コマンドの整合が取れる状態を維持する。

### 14.4 既存 Loss 編集時の標準手順（必須）

既存の `src/models/loss/*.py` を編集する場合は、以下を実施する。

- 最低必須:
  - `uv run pytest tests/test_contrastive_losses.py -q`
  - `uv run pytest tests/test_configs.py -q`
- 入出力変更時の追加必須（曖昧判断を禁止）:
  - `__init__` の入力契約を変更した場合（引数、必須 config キー、初期化時に読むファイル/環境変数、初期化時の例外条件）:
    - `uv run pytest tests/test_configs.py -q`
    - `uv run pytest tests/test_train_integration.py -q`
  - `forward` の入力契約を変更した場合（引数、必須 config キー、shape/dtype 前提、入力ファイル解決規則）:
    - `uv run pytest tests/test_train_integration.py -q`
    - `uv run pytest tests/test_eval.py -q`
  - `forward` の出力契約を変更した場合（戻り値の型・意味、損失値の定義域、例外条件）:
    - `uv run pytest tests/test_train_integration.py -q`
    - `uv run pytest tests/test_eval.py -q`
  - Hydra の multirun/sweep で参照される Loss 設定キーを追加・削除・改名した場合:
    - `uv run pytest tests/test_sweeps.py -q`
  - CUDA 依存分岐、device 固有処理、precision 依存処理を変更した場合:
    - `bash scripts/test.sh`
- OpenSpec change の `tasks.md` には、実施項目と未実施理由を必ず記録する。

## 15. AAPD ラベル説明マッピング生成

- AAPD ラベル埋め込み用途の補助データとして、arXiv taxonomy 原文説明の対応表を生成できるようにする。
- 生成スクリプトは `scripts/build_aapd_arxiv_label_descriptions.py` を使用する。
- 実行コマンド:
  - `uv run python scripts/build_aapd_arxiv_label_descriptions.py`
- 出力先:
  - `data/aapd/arxiv_label_descriptions.json`
- 実装要件:
  - スクリプトは単一ファイルで完結すること。
  - 説明文は要約せず、arXiv から抽出した原文を保存すること。
  - 取得または解析または保存に失敗した場合、途中生成ファイルを削除すること。

## 16. Classification 損失関数の選択

- classification stage model は設定から Hydra instantiate 可能な `criterion` を解決し、`bce`、`asymmetric`、`zlpr` をサポートする。
- classification 設定は単軸 `classification/model=...` を廃止し、`classification/strategy` と `classification/loss` の 2 軸で構成する。
- Hydra の group override では package 指定を明示し、`classification/strategy@classification.model=<name>` と `classification/loss@classification.model=<name>` を使用する。
- classification loss config は `criterion._target_` を持ち、module 内で `loss_name` / `loss_kwargs` の文字列分岐を持たない。
- `criterion._target_=src.models.loss.classification.AsymmetricLoss` 指定時、criterion は Asymmetric Loss として初期化される。
- `criterion._target_=src.models.loss.classification.ZLPRLoss` 指定時、criterion は ZLPR loss として初期化される。
- Asymmetric loss は `gamma_pos`、`gamma_neg`、`margin` を設定から受け取る。
- `gamma_pos=0`、`gamma_neg=1`、`margin=0` 指定時、forward 計算はその値を使う。

## 17. 報告前自己点検ワークフロー

- 作業報告の前に、開発者は `scripts/verify_delivery.sh` を実行して自己点検を行う。
- 自己点検では、OpenSpec change 完了状態、検証コマンド実行結果、commit 情報を確認できる状態を作る。
- `scripts/verify_delivery.sh` は、指定 change の未完了または検証コマンド失敗時に非0で終了する。
- 報告は `docs/delivery_self_check.md` のテンプレートに従い、commit 粒度・実行検証・OpenSpec 状態を必ず含める。

### Requirement: Structured local verification matrix for training changes

Training-related changes MUST distinguish CPU CI reproduction, CPU slow validation, and local GPU validation as separate verification tracks.

#### Scenario: Reproduce required CPU CI locally

- **WHEN** 開発者または coding agent が PR 必須の training-related CI をローカルで再現する
- **THEN** repository 提供の CPU CI 用スクリプトまたは同等コマンドを実行する
- **AND** その pytest 条件は `not slow and not gpu` を満たす

#### Scenario: Run local GPU verification

- **WHEN** 開発者または coding agent が GPU 固有の学習経路を検証する
- **THEN** GitHub hosted runner を前提にせずローカル実機または同等 GPU 環境で実行する
- **AND** `scripts/test.sh` または GPU marker を含む pytest が利用される

### Requirement: GPU-only pytest cases must be explicitly marked

Pytest cases that require visible GPUs SHALL be marked explicitly so CPU CI suites can exclude them deterministically.

#### Scenario: Add a GPU-specific train test

- **WHEN** 開発者または coding agent が GPU availability を前提とする pytest case を追加または更新する
- **THEN** その test には `gpu` marker が付与される
- **AND** CPU CI suite からは marker condition で除外できる
