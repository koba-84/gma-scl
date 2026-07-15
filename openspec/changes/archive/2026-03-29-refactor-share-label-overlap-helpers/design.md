## Context

contrastive loss 群のうち `Base` と `MSC` は label OR-count を private helper で持ち、`MCACR` 系は同じ入力から union-count を別式で直接組み立てています。いずれも multi-hot label set 間の overlap を扱う処理で、責務としては `src/models/loss/components` に置くのが自然です。

## Goals / Non-Goals

**Goals:**

- label overlap 計算の ownership を shared components に寄せる
- `Base`/`MSC`/`MCACR` 系で同じ入力 contract を使う
- 既存の loss API と test 意味論は変えない

**Non-Goals:**

- aggregation や label stats の仕様変更
- loss の数式変更
- `classification.py` の変更

## Decisions

- `src/models/loss/components/label_overlap.py` を新設し、OR-count と union-count を集約する
  - 理由: 既存の `components` 配下の役割に合い、4 モジュール以上で共有するため
- `Base._compute_or` は既存 property test 互換のため薄い staticmethod delegate として残す
  - 理由: class method 自体を public contract にしないが、既存 test を無理に壊さないため
- `MSC` は module 内 helper を削除して shared helper を直接使う
- `MCACR` / `MCACRWONEG` は union の直接式を shared helper に置き換える

## Risks / Trade-offs

- [Risk] helper の抽象化が増える → Mitigation: OR-count と union-count だけに限定し、module-specific 重み計算は各 loss に残す
- [Risk] test が private helper 名へ結びついたまま残る → Mitigation: 既存の `Base._compute_or` だけ薄く残し、新規 test は shared behavior を見る
