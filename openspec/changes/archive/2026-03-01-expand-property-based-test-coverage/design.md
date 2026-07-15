## Context

training spec 13.10 では tests 配下の pytest ファイル名に `test` 語を含めないことを MUST としている。現状は `tests/test_property_based.py` と `tests/test_task_wrapper.py` が残っており、命名規約に不一致である。また、property-based test の次対象は会話で合意済みだが、OpenSpec task へ未記録である。

## Goals / Non-Goals

**Goals:**

- テストファイル名を命名規約へ合わせる。
- property-based test の次対象（3項目）を OpenSpec task として記録する。
- 既存の実行コマンド参照を新ファイル名へ更新する。

**Non-Goals:**

- 今回の change で 3 項目すべてを実装完了すること。
- 既存の固定入力テストを置換すること。

## Decisions

1. `tests/test_property_based.py` を `tests/property_based.py` へ改名する。
2. `tests/test_task_wrapper.py` を `tests/task_wrapper.py` へ改名する。
3. 拡張 task は以下 3 項目を個別管理する。
   - `_log_softmax_temp` の不変条件 property test
   - `Base.forward` の shape/例外契約 property test
   - `compute_gcbs_permutation` の異常入力・境界入力 property test

## Risks / Trade-offs

- [Risk] 参照パスの更新漏れでコマンドが失敗する。
  Mitigation: `rg` で旧パス参照を網羅検索して更新する。
- [Risk] 拡張 task が未着手のまま滞留する。
  Mitigation: tasks.md で 1 項目 1 task とし、優先順を明記する。

## Validation Plan

- `uv run pytest tests/property_based.py -q`
- `uv run pytest tests/task_wrapper.py -q`
- `uv run pre-commit run -a`
