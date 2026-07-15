## Context

contrastive loss 群は Hydra から `loss_fn` として instantiate され、`ContrastiveLitModule` から `loss_fn(z, labels)` ないし `loss_fn(z, labels, prototype=...)` で呼ばれます。公開 API は概ね揃っている一方、実装内では `forward` が全計算を抱えるもの、module-level helper に分けているもの、graph 構築 helper まで同居しているものが混在しています。

また、main spec では `src/models/loss/*.py` の `__main__` 自己テストを単体テストとして規定していますが、現在の repository は pytest 中心で test を維持しており、この契約がノイズになっています。

## Goals / Non-Goals

**Goals:**

- contrastive loss 実装の内部レイアウトを同じ読み順に揃える
- `forward` の責務を入力検証と orchestration に限定する
- 自己テストを pytest に置き換えて、loss 単体検証の入口を統一する
- Hydra target と `ContrastiveLitModule` からの呼び出し契約は維持する

**Non-Goals:**

- `classification.py` の整理
- 各 loss の数式や学習挙動の変更
- `Base` と `MulSupCon` の統合
- MXCLR の graph helper を別 module へ再分割すること

## Decisions

- 各 loss module は「定数 → private helper → public class」の順に揃える
  - 理由: 実装の読み順を統一しつつ、公開 API は最小限に保てるため
  - 代替案として `forward` 完結型へ寄せる案もあるが、MSC / MXCLR / MCACR のような長い数式処理では責務が再び混ざるため採用しない
- loss 本体計算 helper は `_compute_<loss>_loss` 命名で統一する
  - 理由: module 間で同じ検索語で辿れ、`forward` の役割も揃うため
- `MCACRWONEG` は `MCACRLoss` 継承を維持しつつ、shape validation を private helper 化して差分を repulsion 重みだけに寄せる
  - 理由: 公開 class と config を変えずに読みやすさだけ改善できるため
- `__main__` 自己テストは削除し、pytest で module ごとの正常系・異常系・Hydra instantiate を確認する
  - 理由: 現在の test 体系と一致し、spec 上の検証入口も 1 つにできるため

## Risks / Trade-offs

- [Risk] helper への分割で private API が増える → Mitigation: 公開 class 名と `forward` 契約は変えず、helper 名も `_compute_*` に限定する
- [Risk] 自己テスト削除で局所実行の入口が減る → Mitigation: loss 向け pytest を小さく保ち、対象ファイル単位で実行できるようにする
- [Risk] spec が二重管理気味で `*.md` と `spec.md` がずれる → Mitigation: change 完了時に main specs の両方を同時に同期する
