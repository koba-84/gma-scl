## ADDED Requirements

### Requirement: MXCLR-family aggs must support uniform-weight BERTScore F1

MXCLR-family aggregation configs MUST include `BERTScore_F1_Uniform` as a supported agg choice. The uniform variant MUST use the same label similarity matrix construction as `BERTScore_F1`, MUST compute the same F1 harmonic mean from directional scores, and MUST weight every active source label equally instead of using IDF weights.

#### Scenario: Build uniform BERTScore F1 score graph

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr_rank contrastive/model/agg@contrastive.model.loss_fn=BERTScore_F1_Uniform` を compose して `score_graph(labels)` を呼び出す
- **THEN** 実装は `npmi` を自動初期化して agg へ渡す
- **AND** `label_idf` is not required by the agg
- **AND** 出力 score graph は有限値で対称かつ `[0, 1]` 範囲に収まる

#### Scenario: Uniform weighting differs from IDF weighting when label IDF is non-uniform

- **WHEN** 同じ labels, label embeddings, and npmi に対して `BERTScore_F1` and `BERTScore_F1_Uniform` を比較する
- **THEN** `BERTScore_F1` は source label weights として `label_idf` を使用する
- **AND** `BERTScore_F1_Uniform` は active source labels を等重みで平均する

#### Scenario: W&B alias preserves uniform F1 agg name

- **WHEN** `_target_=src.models.loss.agg.bertscore_f1.BERTScoreUniformF1Graph` を含む config を W&B alias 導出へ渡す
- **THEN** `contrastive.model.loss_fn.agg_name` は `BERTScore_F1_Uniform` として記録される
- **AND** `loss_fn.agg` subtree は上書きされない

#### Scenario: Hparams search can select uniform F1 MXCLRRank

- **WHEN** 開発者または coding agent が `hparams_search=mxclr_rank_bertscore_uniform_f1` を compose する
- **THEN** sweep params は `contrastive/model=mxclr_rank` を選択する
- **AND** `contrastive/model/agg@contrastive.model.loss_fn=BERTScore_F1_Uniform` を選択する
- **AND** `lambda_rank` は正値として設定される
