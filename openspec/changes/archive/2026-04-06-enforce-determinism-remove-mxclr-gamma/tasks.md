## 1. OpenSpec Artifacts

- [x] 1.1 proposal、design、delta spec で deterministic 既定化と MXCLR gamma 削除の契約を定義する

## 2. Core Implementation

- [x] 2.1 trainer 既定値を `deterministic: True` に変更し、設定解決テストと関連ドキュメントを更新する
- [x] 2.2 MXCLR と MXCLRRank から `gamma` を削除し、Hydra 設定・pytest・main spec を新契約へ同期する
