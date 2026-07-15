## 1. Hypothesis baseline

- [x] 1.1 dev 依存と品質ドキュメントを更新する
  - `pyproject.toml` の dev group に hypothesis を追加する
  - README の品質チェック手順に Hypothesis 実行コマンドを追記する

## 2. Property-based tests

- [x] 2.1 純関数の不変条件テストを追加する
  - `compute_gcbs_permutation` に対して「順列性・長さ一致・範囲内 index」を検証する
  - `Base._compute_or` に対して「可換性・値域制約」を検証する

## 3. Validation and spec sync

- [x] 3.1 導入検証と main spec 反映を完了する
  - `uv run pytest tests/property_based.py` を成功させる
  - `uv run pre-commit run -a` を成功させる
  - `openspec/specs/dev-quality-tooling/spec.md` へ要件を反映する
