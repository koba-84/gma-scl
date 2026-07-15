## 1. Tooling

- [x] 1.1 dev dependency に vulture を追加し、repository-managed な scan 設定を pyproject.toml に定義する

## 2. Dead Code Cleanup

- [x] 2.1 vulture と参照調査を使って未使用関数を特定し、不要な関数を削除する

## 3. Loss Component Restructure

- [x] 3.1 aggregation helper を components 配下へ統一し、top-level loss aggregation module を削除する
- [x] 3.2 MCACR の label frequency / NPMI 計算を components helper へ移し、transport 公開 helper を 1 つに統合する

## 4. Verification And Spec Sync

- [x] 4.1 対象検証を実行し、main specs へ同期して change を完了させる
