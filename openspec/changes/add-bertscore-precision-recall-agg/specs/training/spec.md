## ADDED Requirements

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
