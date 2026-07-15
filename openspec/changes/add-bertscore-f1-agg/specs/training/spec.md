## ADDED Requirements

### Requirement: MXCLR supports BERTScore F1 aggregation

MXCLR MUST support a new agg choice `BERTScore_F1` in addition to existing agg implementations. `BERTScore_F1` MUST reuse the same label similarity matrix and IDF weighting contract as `idf_chamfer`, but MUST treat the forward directional score as Precision, the reverse directional score as Recall, and MUST return their harmonic mean `2PR / (P + R)` as the pairwise score.

#### Scenario: Build MXCLR score graph with BERTScore F1

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr contrastive/model/agg@contrastive.model.loss_fn=BERTScore_F1` を compose して `score_graph(labels)` を呼び出す
- **THEN** 実装は `npmi` と `label_idf` を自動初期化して agg へ渡す
- **AND** 出力 score graph は有限値で対称かつ `[0, 1]` 範囲に収まる

#### Scenario: Harmonic-mean aggregation differs from idf_chamfer averaging

- **WHEN** 開発者または coding agent が同じ labels と label similarity matrix に対して `idf_chamfer` と `BERTScore_F1` を比較する
- **THEN** `idf_chamfer` は方向別 score の算術平均を返す
- **AND** `BERTScore_F1` は同じ方向別 score を使って `2PR / (P + R)` を返す

### Requirement: W&B logs canonical agg alias for BERTScore F1

When training logs MXCLR hyperparameters to W&B, the derived comparison alias `contrastive.model.loss_fn.agg_name` MUST preserve the canonical name `BERTScore_F1` for the new agg.

#### Scenario: Derive canonical agg alias from BERTScore target

- **WHEN** 開発者または coding agent が `_target_=src.models.loss.agg.bertscore_f1.BERTScoreF1Graph` を含む config を W&B alias 導出へ渡す
- **THEN** `contrastive.model.loss_fn.agg_name` は `BERTScore_F1` として記録される
- **AND** `loss_fn.agg` subtree は上書きされない
