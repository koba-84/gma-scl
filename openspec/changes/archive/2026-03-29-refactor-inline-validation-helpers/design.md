## Context

現在の codebase には `_validate_*` helper が複数ありますが、その大半は 1 箇所からしか呼ばれず、行っている処理も shape / column existence / config guard などの薄い前提確認です。こうした helper は pytest で直接テストする対象でもなく、むしろ主要関数の読解を分断しています。

## Goals / Non-Goals

**Goals:**

- 再利用価値の低い `_validate_*` helper を削除する
- 主要関数の冒頭で前提条件を読めるようにする
- 既存の例外メッセージと失敗条件は維持する

**Non-Goals:**

- 振る舞い変更
- 共有 helper として意味がある数式 helper の削除
- test 方針の再変更

## Decisions

- `mcacr` 系の label shape チェックは `MCACRLoss.forward` と `MCACRWONEG.forward` へ直接書く
- `transport` の shape チェックは `_pairwise_balanced_distance` と `pairwise_transport(strategy='uot')` にそれぞれ inline する
- `tokenized_dataset_cache` の required column チェックは `_tokenize_dataset_dict` に戻す
- `FinetuneLitModule` の encoder config guard は `on_fit_start` に直接書く

## Risks / Trade-offs

- [Risk] 同じ guard が 2 箇所に複製される → Mitigation: 共有対象が 2 箇所未満で、内容も短いものだけ inline する
- [Risk] test が private helper 名に依存している → Mitigation: helper 名を直接使う test は持たず、公開経路で回帰確認する
