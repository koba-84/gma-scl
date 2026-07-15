## Context

現在の property-based test は各テスト関数で `@settings` を直接指定しており、ローカルと CI の探索強度を切り替える統一入口がない。また、失敗再現時の seed/profile 指定手順が README に記載されていない。

## Goals / Non-Goals

**Goals:**

- `tests/conftest.py` で Hypothesis profile（local/ci）を定義し、環境変数で切替可能にする。
- property-based test は profile で共通設定を受け、テスト固有設定を最小化する。
- README に seed/profile の再現手順を追加する。

**Non-Goals:**

- 既存全テストを property-based test へ置換すること。
- Hypothesis の高度設定（database backend 変更など）を導入すること。

## Decisions

1. profile 名を `local` と `ci` に固定する。

- local: `max_examples=120`, `deadline=200`
- ci: `max_examples=240`, `deadline=None`
- 理由: ローカルは速度重視、CI は探索重視で運用を分離する。

2. 有効 profile は `HYPOTHESIS_PROFILE` 環境変数で選択し、未指定時は `local` を使う。

- 理由: pytest コマンド変更なしでも既定挙動が明確になる。

3. 再現手順は pytest オプションとして `--hypothesis-seed` と `--hypothesis-profile` を README に明記する。

- 理由: 失敗の再実行手順をチームで共有できる。

## Risks / Trade-offs

- [Risk] CI の `max_examples` 増加で時間が延びる。
  Mitigation: 対象を `tests/property_based.py` に限定して段階導入する。
- [Risk] profile 指定漏れで意図しない探索強度になる。
  Mitigation: 既定 profile を `local` に固定し、README に切替方法を明記する。

## Validation Plan

- `uv run pytest tests/property_based.py`
- `uv run pytest tests/property_based.py --hypothesis-seed=1 --hypothesis-profile=ci`
- `uv run pre-commit run -a`
