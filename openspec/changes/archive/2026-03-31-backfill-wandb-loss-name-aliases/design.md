## Context

現行の W&B logging は nested config leaf と runtime path を flat alias 化していますが、旧 run 比較で利用していた `*.model.loss_name` のような派生 alias は出力していません。現行 config では loss 名が config key として常に存在するわけではなく、`loss_fn._target_` や `criterion._target_` から導出する必要があります。

## Goals / Non-Goals

**Goals:**

- 現行 config から一意に導ける loss alias を logging と backfill の両方で出力する
- 直近 2 run の `loss_name` 欠損を埋める

**Non-Goals:**

- 旧実装固有で現行 config から一意に導けない alias を復元すること
- `loss_name` 以外の曖昧な派生キーを追加すること

## Decisions

1. alias は `_target_` から明示マッピングで導く。
   class 名の自動 snake_case 化だと `MulSupCon` のような名前が既存比較キーと一致しません。config group 名に対応する明示マッピングを持ちます。

2. backfill は欠損時のみ更新する。
   既に記録済みの run を上書きせず、`None` または空欄のときだけ追加します。

## Risks / Trade-offs

- [Risk] 新しい loss 実装追加時に alias map を更新し忘れる → Mitigation: logging と backfill で同じ明示マッピングを持ち、テストで代表ケースを固定する
- [Risk] 旧 run 固有 alias を過剰に推定する → Mitigation: 現行 config から一意に導ける `loss_name` のみに限定する
