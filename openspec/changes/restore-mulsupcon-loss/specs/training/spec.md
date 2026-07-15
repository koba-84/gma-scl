## MODIFIED Requirements

### Requirement: Contrastive loss 実装の命名

- contrastive loss 実装は可読性のため簡潔で一貫した命名を使用する。
- loss 実装ファイル名は `src/models/loss/<loss_name>.py` の形式に統一し、`loss_` などの冗長な接頭辞を付けない。
- base loss の公開クラス名は `Base` とする。
- supcon loss の公開クラス名は `MulSupCon` とする。
- `MulSupCon` は batch 中の各正ラベルを個別 anchor row に展開し、そのラベルを持つ他サンプル集合に対する supervised contrastive objective を計算する。
- `MulSupCon` の最終 loss は、展開された label-wise rows の平均で集約する。
- MCACR 派生 loss の公開クラス名として `MCACRWONEG` を提供し、負例項ではラベル由来重みを使わない実装を提供する。
- MSC loss の公開クラス名として `MSC` を提供する。
- `MCACRLoss` は `data_dir` と `dataset_name` を受け取り、内部で `<data_dir>/<dataset_name>/train.csv` を解決して初期化時に毎回 NPMI 行列を直接計算する。
- 共通集約契約: labels 集約は初期化引数 `agg`（`mean` / `self_norm` / `chamfer`）で切り替える。
- 共通集約契約（mean）: `sim_mean = (y_i^T S y_j) / (|y_i||y_j|)`。
- 共通集約契約（self_norm）: `w_ij = y_i^T S y_j` と `sim_self = w_ij / sqrt(max(w_ii, eps) * max(w_jj, eps))`。
- 共通集約契約（chamfer）: `sim_chamfer(i,j)=0.5*(r(i→j)+r(j→i))`、`r(i→j)=(1/|Y_i|)*Σ_{a∈Y_i} max_{b∈Y_j} S[a,b]`。
- 共通集約契約（数値制約）: 出力は有限値とし、必要に応じて [0, 1] にクリップする。
- contrastive loss へ渡す埋め込みの L2 正規化は `src/models/contrastive_module.py` の `ContrastiveLitModule._project` で実施する。
- loss 実装側（例: `src/models/loss/mxclr.py`）は埋め込み正規化を重複実装しない。
- MCACR 系 loss（MCACR / MCACRWONEG）は、アンカーに正例が存在しない場合にのみ repulsion 項を 0 化する。
- `configs/contrastive/model/base.yaml` の `loss_fn._target_` は `src.models.loss.base.Base` を参照する。
- `configs/contrastive/model/ml_supcon.yaml` の `loss_fn._target_` は `src.models.loss.ml_supcon.MulSupCon` を参照する。
- `configs/contrastive/model/mcacr_woneg.yaml` の `loss_fn._target_` は `src.models.loss.mcacr_woneg.MCACRWONEG` を参照する。
- `configs/contrastive/model/mxclr.yaml` の `loss_fn._target_` は `src.models.loss.mxclr.MXCLR` を参照する。
- `configs/contrastive/model/msc.yaml` の `loss_fn._target_` は `src.models.loss.msc.MSC` を参照する。
- MXCLR は標準経路で `loss_fn(z, labels)` を受け取り、内部で `score_graph(labels)` を使って sample-pair score 行列へ変換する。
- MXCLR は `data_dir/<dataset_name>/label_descriptions.json` を読み込んで Sentence-BERT でラベル間意味類似度行列を常時構築する。
- MXCLR はラベル説明文エンコード長 `sbert_max_length` を明示設定で受け取り、初期化時に正値検証したうえで `SentenceTransformer.max_seq_length` へ適用する。
- MXCLR の `score_graph(labels)` は similarity family では共通集約契約（`agg`）の出力をそのまま返し、transport family では pairwise transport distance を `[0, 1]` score に写像して返す。
- MXCLR の loss 本体は batch 内候補 cross entropy をそのまま集計し、focal-style weighting 用の追加ハイパーパラメータを公開契約に含めない。
- distill 系 MXCLR agg は `centering=mean` と `centering=sinkhorn_knopp` の両方を受け付け、どちらでも有限な `[0, 1]` score graph を返す。
- distill 系 MXCLR agg は `lambda_koleo` を受け付け、KoLeo regularizer の前にラベル埋め込みを L2 normalize する。
- MXCLR は `forward(z, labels)` の distill 系 labels 経路に限って KoLeo regularizer を加算し、`forward(z, g_soft)` の direct graph 経路では追加しない。
- MCACR の repulsion 類似度集約も共通集約契約（`agg`）に従い、後段で `repulse_weight = (1-sim)^beta` を適用する。
- MXCLR は semantic 初期化設定が不正（説明ファイル不在、ラベル数不一致など）の場合、学習開始前に初期化例外を送出する。
- MSC は標準経路で `loss_fn(z, labels, prototype)` を受け取り、`ContrastiveLitModule` が保持する学習可能 prototype を正規化して明示供給する。prototype 未指定時は例外を送出する。
- `classification.py` を除く contrastive loss module は、`forward` を入力検証と orchestration に限定し、loss 本体計算は module-level private helper へ委譲する。
- loss 本体 helper の命名は `_compute_<loss>_loss` に統一する。
- `Base` `MSC` `MCACR` 系で共有する label overlap の OR-count / union-count は `src/models/loss/components/label_overlap.py` の shared helper を使い、top-level loss module ごとに重複実装しない。
- 単純な shape / config / column existence の guard は、pytest で独立に守る helper として切り出さず、主要関数の冒頭へ直接記述する。

#### Scenario: supcon loss クラスを構成から解決する

- **WHEN** `configs/contrastive/model/ml_supcon.yaml` の `loss_fn._target_` を使ってインスタンス化する
- **THEN** `src.models.loss.ml_supcon.MulSupCon` が解決され、学習時に利用できる

#### Scenario: MulSupCon computes label-wise expanded supervised contrastive loss

- **WHEN** `MulSupCon.forward(z, labels)` が multi-label batch に対して呼ばれる
- **THEN** batch 中の各正ラベルは個別 anchor row に展開される
- **AND** 各 row は同じラベルを持つ他サンプルを positives として supervised contrastive loss を計算する
- **AND** 最終 loss は展開された label-wise rows を平均した有限スカラーになる
