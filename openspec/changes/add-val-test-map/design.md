## Overview

既存の classification stage は `torch.sigmoid(logits) >= 0.5` を用いた二値予測で F1/hamming loss を計算している一方、mAP は threshold 後の 0/1 予測ではなく確率スコアを入力に取る必要があります。そのため batch ごとに logits から sigmoid score を作り、F1 系とは分離して `MultilabelAveragePrecision` を更新します。

## Decisions

- val/test の mAP は `torchmetrics.classification.MultilabelAveragePrecision` を使う
- mAP 更新には二値化前の `scores = torch.sigmoid(logits)` を使う
- 既存の F1/hamming loss の計算経路と checkpoint monitor は変更しない
- 追加ログ名は `classification/val/map` と `classification/test/map` に固定する

## Alternatives Considered

- `AveragePrecision(task="multilabel", ...)` を使う案
  - task dispatch よりも multi-label 専用 class の方が意図が明確なため不採用
- mAP を checkpoint monitor に使う案
  - 既存契約と比較軸を変えるため今回は不採用

## Validation

- `uv run pytest tests/test_eval.py tests/test_configs.py`
- `uv run pre-commit run -a`
