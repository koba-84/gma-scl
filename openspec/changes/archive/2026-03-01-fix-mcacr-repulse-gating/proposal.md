## Why

MCACR 系実装では、repulsion 項の無効化条件が loss_attract == 0 になっている。これにより、正例が存在していても正例距離が 0 の場合に repulsion まで 0 化され、目的関数の意図とずれる。

## What Changes

- MCACR と MCACR_WONEG の repulsion 無効化条件を、attraction loss 値ではなく「正例の有無」に変更する。
- 正例がないアンカーのみ repulsion を 0 にする。
- 回帰テストを追加し、正例があるが attraction 距離が 0 のケースで repulsion が有効なままになることを検証する。

## Capabilities

### Modified Capabilities

- training: MCACR 系 loss のアンカー単位ゲート条件を、正例有無ベースに修正する。

## Impact

- 影響コード: src/models/loss/mcacr.py, src/models/loss/mcacr_woneg.py, tests/test_mcacr_woneg.py
- 正例が存在する一部ケースで loss 値が 0 から非 0 に変化する。
