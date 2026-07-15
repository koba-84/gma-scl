## 1. OpenSpec Artifacts

- [x] 1.1 proposal、design、delta spec で MXCLR gamma の目的・契約・設計を定義する

## 2. Core Implementation

- [x] 2.1 `src/models/loss/mxclr.py` に `gamma` 引数、focal-style weighting、値検証を追加し、`configs/contrastive/model/mxclr.yaml` と MXCLR テスト群を更新する

## 3. Verification

- [x] 3.1 MXCLR 関連 pytest と Hydra 設定解決で変更を検証し、main spec (`openspec/specs/training/spec.md`) へ要件を同期する
