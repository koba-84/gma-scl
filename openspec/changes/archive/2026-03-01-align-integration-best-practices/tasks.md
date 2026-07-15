## 1. OpenSpec artifacts

- [x] 1.1 proposal を作成し、統合テスト改善対象と命名変更対象を定義する
- [x] 1.2 design を作成し、data quality/reproducibility テスト方針を定義する
- [x] 1.3 training delta spec を作成し、fast integration 要件と命名規約を追加する

## 2. Implementation

- [x] 2.1 fast integration に data quality（簡易 skew 検証）テストを追加する
- [x] 2.2 fast integration に reproducibility（固定 seed）テストを追加する
- [x] 2.3 tests 配下のファイル名から `test` 語を除去する
- [x] 2.4 CI ワークフローを fast/slow 分離運用に更新する
- [x] 2.5 fast integration に data schema 契約（split 列不一致）検知テストを追加する
- [x] 2.6 fast integration に contrastive→classification artifact 引き渡し契約テストを追加する

## 3. Verification and review

- [x] 3.1 `uv run pytest --collect-only -q` で収集が成立することを確認する
- [x] 3.2 `uv run pytest -m "not slow" -q` で通過確認する
- [x] 3.3 追加/変更テストをセルフレビューし、OpenSpec main spec を同期する
