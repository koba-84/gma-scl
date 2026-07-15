# 学習仕様（Training Spec）

## 0. 前提（環境と実行）

- 実行は必ず uv 仮想環境を使用する（`.venv/bin/python3`）。
- 実行は必ず `uv run ...` 経由で行う。
- 依存追加・更新は必ず `uv add ...` を使用する。
- pip / conda による依存インストール手順は採用しない。

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
  - `seed=0` は有効な固定値として扱われ、`lightning.seed_everything(0, workers=True)` が実行される。

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
- MXCLR loss の公開クラス名として `MXCLR` を提供する。
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
- MXCLRRank は MXCLR の agg group 契約をそのまま再利用し、`BERTScore_F1` `BERTScore_F1_Uniform` `BERTScore_Precision` `BERTScore_Recall` を含む既存 agg config を `contrastive/model/agg@contrastive.model.loss_fn=...` で選択できる。
- `configs/hparams_search/mxclr_rank_bertscore_uniform_f1.yaml` は MXCLRRank で `BERTScore_F1_Uniform` を選択し、ranking 項を有効化するため `lambda_rank` を正値に設定する。
- MXCLRRank の ranking 項は row-wise ListMLE を使い、`mxclr_loss + lambda_rank * listmle_loss` として計算する。
- MXCLRRank の ListMLE ranking 項は `rank_temperature` で student scores を scaling し、MXCLR soft-target loss 側の `instance_temperature` とは独立に制御する。
- MXCLRRank は ranking 項に batch size による追加正規化を入れない。
- MXCLR は `data_dir/<dataset_name>/label_descriptions.json` を読み込み、Sentence-BERT でラベル間意味類似度行列を構築する。
- MXCLR は独立した `label_description_path` 引数を公開しない。
- MXCLR はラベル説明文エンコード長 `sbert_max_length` を明示設定で受け取り、初期化時に正値検証したうえで `SentenceTransformer.max_seq_length` へ適用する。
- MXCLR の `score_graph(labels)` は共通集約契約（`agg`）の出力をそのまま返す。
- MXCLR-family loss は agg-level regularizer hook を呼び出さず、labels 経路でも graph 直入力経路でも score graph 由来の contrastive objective のみを計算する。
- MXCLR は semantic 初期化設定が不正（説明ファイル不在、ラベル数不一致など）の場合、学習開始前に初期化例外を送出する。
- MSC は標準経路で `loss_fn(z, labels, prototype)` を受け取り、`ContrastiveLitModule` が保持する学習可能 prototype を正規化して明示供給する。prototype 未指定時は例外を送出する。
- `classification.py` を除く contrastive loss module は、`forward` を入力検証と orchestration に限定し、loss 本体計算は module-level private helper へ委譲する。
- loss 本体 helper の命名は `_compute_<loss>_loss` に統一する。
- `Base` `MSC` で共有する label overlap の OR-count / union-count は `src/models/loss/components/label_overlap.py` の shared helper を使い、top-level loss module ごとに重複実装しない。
- 単純な shape / config / column existence の guard は、pytest で独立に守る helper として切り出さず、主要関数の冒頭へ直接記述する。

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
- 追加契約:
  - contrastive から classification への `pretrained_encoder_path` 注入が成立することを確認する。
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
  - ラベル分布の簡易 skew と span 間 drift を tiny データで検知する。
  - split 間の列契約（schema 不一致）を tiny データで検知する。
  - 固定 seed 条件で DPP 経路の再現性を確認する。
- 実行例:
  - `uv run pytest tests/test_data_integration.py -q`
  - `uv run pytest -m integration tests/test_data_integration.py -q`

### 13.10 pytest ファイル命名規約

- tests 配下の collected pytest module は pytest 標準 discovery 命名（`test_<topic>.py` または `<topic>_test.py`）を MUST 採用する。
- support code は `tests/support/` など collected test modules とは別の領域へ置く。

### 13.11 ローカル検証運用規約（pre-commit 中心）

- commit/push 前の必須チェックは `uv run pre-commit run -a` とする。
- fast テスト（`-m "not slow"`）は追加検証として推奨する。
- slow テスト（`-m "slow"`）は必要時に手動実行する。

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
- 4. GPU 実機確認（学習ループ、GPU 専用処理、trainer、data runtime を変更した場合のみ）:
  - `bash scripts/test.sh`
- loss 数式、Hydra loss config、または CPU で完結する loss 単体挙動だけを変更した場合、`scripts/test.sh` は必須検証に含めない。

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
  - `${paths.root_dir}/data/aapd/label_descriptions.json`
- 実装要件:
  - スクリプトは単一ファイルで完結すること。
  - 説明文は要約せず、arXiv から抽出した原文を保存すること。
  - 取得または解析または保存に失敗した場合、途中生成ファイルを削除すること。
