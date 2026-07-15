## Context

現在の `configs/contrastive/train.yaml` は `contrastive/model@model: ml_supcon` を既定値としている。一方、比較実験では base loss を基準に扱う運用が多く、都度 override が必要で設定ミスの余地がある。さらに、contrastive epoch の比較を定型化した hparams_search が未整備である。

## Goals / Non-Goals

**Goals:**

- contrastive 既定 model を base loss に統一する。
- contrastive epoch を 1, 5, 10, 20 で自動 sweep できる設定を追加する。
- 実装内容を training spec に反映し、運用ルールを明文化する。

**Non-Goals:**

- loss 実装本体（`src/models/loss/*`）のアルゴリズム変更。
- test1 から test4 の既存探索軸の変更。
- classification 側の学習長や最適化仕様の変更。

## Decisions

- Decision 1: `configs/contrastive/train.yaml` の `contrastive/model@model` を `base` に変更する。

  - Rationale: 既定挙動を実験基準に合わせ、コマンド override の頻度と設定ミスを減らす。
  - Alternative: 既定は据え置きで README のみ更新。却下理由: 実行時の実害（指定漏れ）を防げない。

- Decision 2: 新規 `configs/hparams_search/contrastive_epoch.yaml` を追加し、`contrastive.trainer.max_epochs: 1,5,10,20` を定義する。

  - Rationale: 既存 test1 から test4 を汚さず、目的特化の sweep を分離できる。
  - Alternative: test1 から test4 に epoch 軸を混在。却下理由: 既存比較軸が不明瞭になる。

- Decision 3: epoch sweep は classification 設定を上書きせず、既定どおり下流評価まで実行する。

  - Rationale: 実験評価の主目的は下流タスク性能であり、比較条件は classification を含めてそろえる必要がある。
  - Alternative: classification を無効化して contrastive-only で回す。却下理由: 下流指標が得られず評価要件を満たせない。

## Risks / Trade-offs

- [Risk] 既定 loss の切替で過去コマンドの結果解釈が混在する。→ Mitigation: spec に明記し、明示 override 例を残す。
- [Trade-off] epoch sweep 1回あたりの計算時間は増える。→ Mitigation: seed や dataset を固定し、比較軸を epoch のみに限定して運用する。
