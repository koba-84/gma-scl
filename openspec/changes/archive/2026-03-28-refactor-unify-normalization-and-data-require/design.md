## Context

現在の学習コードでは、L2 正規化が normalize_embeddings、_normalize_prototype、functional.normalize に分かれて実装されています。いずれも行列の行方向正規化という同一目的であり、専用 helper を経由する価値よりも読解コストの方が大きい状態です。

classification datamodule でも train/val/test ごとに同型の存在確認 helper を持っており、分岐追加時に修正点が増える構造になっています。

## Goals / Non-Goals

**Goals:**
- 正規化処理を functional.normalize に寄せて実装意図を 1 つに揃える
- datamodule のデータ存在確認を単一 helper に集約して重複をなくす
- 挙動を変えずに可読性と保守性を上げる

**Non-Goals:**
- 損失計算式や dataloader の外部契約を変更しない
- 新しい抽象化レイヤーや互換分岐を追加しない

## Decisions

- 正規化 helper のうち、単純な wrapper しか提供していないものは削除し、呼び出し側で functional.normalize を直接使う
  - 代替案として共通 utility への集約もあるが、1 行処理を別名にするだけで追跡経路が増えるため採用しない
- prototype 正規化は contrastive module 内で tensor の device/dtype 調整後にそのまま functional.normalize を適用する
  - 既存の型・device 整合性は維持する
- classification datamodule は split 名を受け取る単一 helper で train/val/test を解決する
  - 代替案として property 化もあるが、既存 call site が dataloader 毎に明示的な split を持つため helper 集約だけに留める

## Risks / Trade-offs

- 正規化 helper 削除に伴い型変換位置を誤ると数値差分が入り得る → 既存と同じ dtype/device 変換順を維持し、対象テストで確認する
- 共通 split helper によるエラーメッセージ変更で既存テストが壊れる可能性がある → split 名を含む明示的なメッセージを維持する

## Migration Plan

- ローカル topic branch でリファクタを適用する
- 対象テストと pre-commit を通した後に task 単位で commit する
- PR を作成し、レビュー可能な単位で main に merge する

## Open Questions

- なし
