## Context

`BERTScore_F1` は `idf_chamfer` と同じ方向別 IDF score を使い、Precision/Recall の調和平均を返します。一方で、研究比較では方向別 score そのものを観測したい場面があり、`BERTScore_F1` だけでは source→target と target→source の差分を直接評価できません。

今回の変更では、既存 `BERTScore_F1` の書き方を踏襲しつつ、共通計算を保ったまま `BERTScore_Precision` と `BERTScore_Recall` を追加する必要があります。また、Precision と Recall は本質的に有向 score なので、対称 score を前提にしたテスト契約をそのまま流用しないよう明示する必要があります。

## Goals / Non-Goals

**Goals:**

- MXCLR に新しい agg `BERTScore_Precision` と `BERTScore_Recall` を追加する
- `BERTScore_F1` と同じ similarity matrix / IDF weighting から方向別 score を再利用する
- W&B alias と Hydra compose で canonical 名を保持する
- Precision/Recall が転置関係になることをテストで検証する

**Non-Goals:**

- `BERTScore_F1` や `idf_chamfer` の数式変更
- Precision/Recall を対称化して既存 chamfer 系と同じ意味に寄せること
- MCACR 側の agg 契約拡張

## Decisions

1. 共通ロジックは `bertscore_f1.py` から切り出さず、同ファイル内に補助関数を追加して `BERTScoreF1Graph` / `BERTScorePrecisionGraph` / `BERTScoreRecallGraph` で共有する
   - Rationale: BERTScore 系 agg の実装差分を 1 ファイルに閉じ、既存実装との比較を容易にする
   - Alternative considered: 新しい共通 util module を追加する
   - Rejected because: 今回の共有範囲が狭く、ファイル分割の利益が小さい

2. `BERTScore_Precision` は source 文書の IDF 重み付き directional score をそのまま返し、`BERTScore_Recall` はその転置を返す
   - Rationale: `BERTScore_F1` が使う Precision/Recall の定義をそのまま独立観測できる
   - Alternative considered: Recall 側で別計算パスを持つ
   - Rejected because: 同一 similarity matrix 上では Recall は Precision の転置で十分に定義できる

3. property test は新規 agg だけ対称性チェックを外し、`precision_graph == recall_graph.T` を確認する
   - Rationale: Precision/Recall の有向性を仕様として固定できる
   - Alternative considered: 既存一括 parametrized test に対称性例外分岐を増やさない
   - Rejected because: 新規 agg の契約差分が見えにくくなる

## Risks / Trade-offs

- [Risk] 有向 graph を loss に渡すことで既存の「対称 graph 前提」理解と衝突する
  Mitigation: OpenSpec と pytest に非対称許容と Precision/Recall の転置関係を明記する
- [Risk] alias 追加漏れで W&B comparison 列が snake_case に崩れる
  Mitigation: alias helper と backfill/logging テストに canonical 名ケースを追加する
