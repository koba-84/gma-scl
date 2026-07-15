## Context

現在の集約契約は `mean` と `self_norm` のみで、MXCLR と MCACR の双方に同型ロジックが重複実装されている。今回の `chamfer` はラベル集合間の全ペア平均ではなく、各ラベルの最良対応のみを使うため、方向付き近傍平均と対称化が必要になる。

## Goals / Non-Goals

**Goals:**

- `agg` に `chamfer` を追加し、MXCLR/MCACR の両方で同一定義を使う。
- 既存 `mean`/`self_norm` の数値挙動を変更しない。
- 実装を共通関数化して将来の集約追加時の重複を減らす。

**Non-Goals:**

- `chamfer_min` や `chamfer_geom` など別バリアントの追加。
- 既存設定の既定値変更。
- loss 本体の attract/repulse 温度や指数パラメータ定義の変更。

## Decisions

1. 集約ロジックを `src/models/loss` 内の共通関数へ切り出し、`mean`/`self_norm`/`chamfer` を一元実装する。

- 理由: MXCLR と MCACR の重複実装を避け、数式差分をなくす。
- 代替案: それぞれのファイルで同じ `chamfer` を個別実装する。
  - 不採用理由: 将来の修正漏れリスクが高い。

2. `chamfer` の定義は次式で固定する。

- `Y_i={a | y_i[a]=1}`, `Y_j={b | y_j[b]=1}`
- `r(i→j)= (1/|Y_i|) * Σ_{a∈Y_i} max_{b∈Y_j} S[a,b]`
- `r(j→i)= (1/|Y_j|) * Σ_{b∈Y_j} max_{a∈Y_i} S[a,b]`
- `sim_chamfer(i,j)=0.5*(r(i→j)+r(j→i))`

- 理由: ユーザー要求の `chamfer_mean` に一致し、対称行列として扱える。
- 代替案: `min` や幾何平均での対称化。
  - 不採用理由: 今回要件外。

3. 数値安全策として、ラベル数 0 は `clamp_min(1)` で除算保護し、出力は既存同様 `[0,1]` にクリップする。

- 理由: 既存契約との整合を維持する。

## Risks / Trade-offs

- [Risk] `chamfer` は `mean` より計算コストが高く、バッチやラベル数が大きいと forward 時間が増える。
  Mitigation: バッチ内演算のテンソル化を維持し、Python ループを避ける。
- [Risk] ラベルが極端に疎なデータでは `chamfer` が高めの類似を返しやすい場合がある。
  Mitigation: 既存 `mean`/`self_norm` を残し、設定で比較可能にする。
