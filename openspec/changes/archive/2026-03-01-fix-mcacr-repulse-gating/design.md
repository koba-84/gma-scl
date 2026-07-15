## Context

MCACR と MCACR_WONEG はともに、アンカーごとの repulsion 項を最後にゲートしている。現行実装は loss_attract == 0 を判定に使っており、これは「正例がない」ことと同値ではない。

## Goals / Non-Goals

Goals:

- repulsion の無効化を「正例がないアンカー」に限定する。
- MCACR と MCACR_WONEG の整合を保つ。
- 変更を最小差分に留める。

Non-Goals:

- attraction / repulsion の重み定義変更。
- 温度やハイパーパラメータ探索範囲の変更。

## Decisions

1. ゲート条件は attract_mask.any(dim=1) を用いる。
   理由: 「正例が存在するか」を直接表現でき、loss 値に依存しない。

2. loss_attract == 0 判定は廃止する。
   理由: 距離 0 による偶発的ゼロと、正例不在を分離するため。

3. テストは forward 出力の符号で回帰を検出する。
   理由: 旧実装では 0、新実装では負値になる最小ケースを作れるため。

## Risks / Trade-offs

- 正例距離 0 のバッチで従来より強い repulsion が効く。
  - Mitigation: これは意図した挙動であり、テストで固定する。
