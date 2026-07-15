## 1. OpenSpec Artifacts

- [x] 1.1 proposal.md を作成し、命名短縮の目的と破壊的変更を定義する
- [x] 1.2 specs/training/spec.md で base loss 命名要件の変更を定義する
- [x] 1.3 design.md で実装方針とトレードオフを定義する

## 2. Loss Naming Refactor

- [x] 2.1 `src/models/loss/base.py` のクラス名を `Base` に変更する
- [x] 2.2 `src/models/loss/__init__.py` の公開名を `Base` に更新する
- [x] 2.3 `configs/contrastive/model/base.yaml` の `_target_` を新クラス名へ更新する
- [x] 2.4 `src/models/loss/ml_supcon.py` のクラス名を `MulSupCon` に変更する
- [x] 2.5 `configs/contrastive/model/ml_supcon.yaml` の `_target_` を新クラス名へ更新する
- [x] 2.6 `src/models/loss/__init__.py` の supcon 公開名を `MulSupCon` に更新する

## 3. Verification

- [x] 3.1 リポジトリ内の旧クラス名参照を検索し、必要箇所を更新する
- [x] 3.2 他 loss（`MCACRLoss`）の命名状況を確認して報告する
