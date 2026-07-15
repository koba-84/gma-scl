## 1. Profile baseline

- [x] 1.1 Hypothesis profile を共通設定として追加する
  - `tests/conftest.py` で local/ci profile を登録する
  - `HYPOTHESIS_PROFILE` 未指定時は local を読込む

## 2. Property test alignment

- [x] 2.1 property-based test を profile 運用に合わせる
  - `tests/property_based.py` の `deadline=None` を削除する
  - 探索回数はテスト固有要件のみ残す

## 3. Repro guidance and spec sync

- [x] 3.1 再現手順の文書化と main spec 反映を行う
  - README に seed/profile を使った再現コマンドを追記する
  - `openspec/specs/dev-quality-tooling/spec.md` に要件を反映する
  - `uv run pytest tests/property_based.py` と `uv run pre-commit run -a` を成功させる
