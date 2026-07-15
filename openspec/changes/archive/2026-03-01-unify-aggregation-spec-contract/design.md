## Context

現在は MCACR と MXCLR で同一の agg 式が重複している。仕様統合のベストプラクティスとして、共通ルールは1箇所で管理し、個別仕様は参照に寄せる。

## Goals / Non-Goals

**Goals:**

- agg 分岐の定義を共通契約へ統合する。
- 個別仕様は責務差分のみ記述する。

**Non-Goals:**

- 実装式の変更。
- 新しい agg モードの追加。

## Decisions

1. training main spec に共通契約ブロックを追加し、許可値・式・数値制約を定義する。
2. MCACR/MXCLR 個別行は「どの場面で共通契約を使うか」の責務記述へ縮約する。
3. change specs も同様に重複式記載を削減して参照形式にする。

## Risks / Trade-offs

- [Risk] 参照先が不明瞭だと可読性が下がる。
  Mitigation: 参照元ファイル・節名を明記する。
