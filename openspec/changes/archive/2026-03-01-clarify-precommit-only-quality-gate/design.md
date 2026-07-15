## Context

既存仕様には push 前 `uv run pytest -m "not slow"` の必須要件が残っているが、現在の運用意図は pre-commit を主品質ゲートにすること。個人開発では検証の即時性と運用コストの両立が重要であり、必須要件は pre-commit に集約し、pytest は推奨運用へ整理する。

## Goals / Non-Goals

**Goals:**

- pre-commit 成功を必須ゲートとして仕様に明記する。
- push 前 pytest の要件を推奨へ変更する。
- commit 粒度の規約は維持する。

**Non-Goals:**

- テストコードや学習コードの挙動変更。
- CI 導入要件の追加。

## Decisions

1. 必須品質ゲートは `uv run pre-commit run -a` とする。
2. `uv run pytest -m "not slow"` は推奨検証として扱う。
3. commit/push 粒度規約は既存のまま維持する。

## Risks / Trade-offs

- [Risk] pytest を必須から外すことで push 前の実行網羅が下がる。
  - Mitigation: 重要変更時は追加検証として pytest を推奨し、仕様にも推奨として残す。

## Migration Plan

1. 仕様（version-control/training/dev-quality）を更新する。
2. 仕様差分を main specs に反映する。
3. 変更内容を粒度分離して commit する。

## Open Questions

- 将来 CI を再導入する場合、pre-commit と pytest の必須/推奨の境界を再定義する。
