## Context

contrastive 用 loss は `base`, `ml_supcon`, `mcacr` の 3 実装があり、クラス名はそれぞれ `BaseMultiLabelContrastiveLoss`, `MultiLabelSupConLoss`, `MCACRLoss` となっている。`base` と `ml_supcon` の命名が長く、設定記述と import 名の視認性が低い。

## Goals / Non-Goals

**Goals:**

- base loss クラス名を `Base` に短縮する。
- supcon loss クラス名を `MulSupCon` に短縮する。
- 設定と公開 API（`__init__.py`）の参照名を `Base` / `MulSupCon` に揃える。
- `MCACRLoss` の命名状況を確認可能な状態にする。

**Non-Goals:**

- `ml_supcon` と `mcacr` のアルゴリズム変更。
- 旧クラス名との後方互換層追加。

## Decisions

- `src/models/loss/base.py` のクラス名を `Base` に変更する。
- `src/models/loss/ml_supcon.py` のクラス名を `MulSupCon` に変更する。
- `configs/contrastive/model/base.yaml` の `_target_` は `src.models.loss.base.Base` に更新する。
- `configs/contrastive/model/ml_supcon.yaml` の `_target_` は `src.models.loss.ml_supcon.MulSupCon` に更新する。
- `src/models/loss/__init__.py` の公開名を `Base`, `MulSupCon` に更新する。
- 互換 alias は追加しない。研究用途ルールに従い曖昧な二重命名を避ける。

## Risks / Trade-offs

- [Risk] 外部コードが旧名 `BaseMultiLabelContrastiveLoss` を import している場合に壊れる。→ Mitigation: 変更内容を明示し、必要なら呼び出し側を同時修正する。
- [Risk] 外部コードが旧名 `MultiLabelSupConLoss` を import している場合に壊れる。→ Mitigation: 変更内容を明示し、必要なら呼び出し側を同時修正する。
- [Trade-off] クラス名が短く一般名詞化する。→ Mitigation: モジュールパス `src.models.loss.base` で文脈を保持する。
