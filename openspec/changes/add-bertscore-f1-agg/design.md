## Context

`IdfChamferGraph` はラベル集合間の方向別 IDF score を計算した後、`0.5 * (forward + backward)` で対称化しています。一方、BERTScore の一次実装は Precision と Recall を別々に計算し、最終 score を `2PR / (P + R)` とするため、現在の agg は名前に反して BERTScore そのものではありません。

今回の変更では、既存の `idf_chamfer` を壊さず、新しい agg として BERTScore 由来の F1 集約を追加する必要があります。また、研究比較で使う W&B alias は実験名として `BERTScore_F1` をそのまま残せる必要があります。

## Goals / Non-Goals

**Goals:**

- MXCLR に新しい agg `BERTScore_F1` を追加する
- `BERTScore_F1` で方向別 IDF score を Precision/Recall として扱い、調和平均で score graph を構築する
- Hydra config と W&B alias の両方で canonical 名 `BERTScore_F1` を扱えるようにする

**Non-Goals:**

- 既存 `idf_chamfer` や `distill_idf_chamfer` の数式変更
- MCACR 側の agg 契約拡張
- BERTScore の baseline rescaling や multi-layer score の導入

## Decisions

1. 新規実装は `src/models/loss/agg/bertscore_f1.py` に `BERTScoreF1Graph` として追加し、`IdfChamferGraph` は変更しない
   - Rationale: 既存実験の再現性を壊さず、比較対象として明確に分離できる
   - Alternative considered: `idf_chamfer` 自体を BERTScore 互換に変更する
   - Rejected because: 既存 run 名と過去結果の意味が変わる

2. `BERTScore_F1` は `idf_chamfer` と同じ similarity matrix と IDF 重みを使い、方向別 score を `P` と `R` に割り当てて `2PR/(P+R)` を返す
   - Rationale: 元論文・公式実装の集約式に最も近い差分で追加できる
   - Alternative considered: 単純平均のまま alias だけ `BERTScore_F1` に変える
   - Rejected because: 挙動が名称と一致しない

3. W&B alias 導出は `_target_` 文字列から module 名を機械的に抜くのではなく、known agg target に対する canonical name mapping を優先する
   - Rationale: Python module 名は snake_case 制約を受ける一方、比較軸では `BERTScore_F1` の表記を保持したい
   - Alternative considered: Python module file を `BERTScore_F1.py` にする
   - Rejected because: Python naming policy と整合しない

## Risks / Trade-offs

- [Risk] `P + R = 0` のペアで NaN が発生する
  Mitigation: 公式実装と同様に safe divide 後の非有限値を 0 に置き換える
- [Risk] alias 導出ルールを変えると既存 agg 名に影響する
  Mitigation: explicit mapping は新規 target のみ追加し、既存 target は現行の module-name fallback を維持する
