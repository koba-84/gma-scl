## Context

現行 workflow には以下の問題がある。

- `test.yml` は workflow 内に直接 pytest コマンドを書いており、ローカル再現用の単一入口がない。
- `uv run pytest -m "not slow"` は GPU が利用可能なローカル環境では `@run_if(min_gpus=1)` の fast GPU test を実行し、CPU CI と同じ意味にならない。
- `code-quality-main.yaml` は旧 `pre-commit/action` に依存し、`code-quality-pr.yaml` と実装が分岐している。
- 失敗時に pytest の JUnit やログを残さず、ML 系の flaky failure や dependency drift の調査効率が低い。
- workflow 全体の concurrency と permissions が粗く、不要な同時実行や広い権限を許している。

外部調査では、GitHub Actions 公式 docs が workflow concurrency / path conditions / artifact retention を明示しており、`setup-python` と `setup-uv` の README も cache key と明示バージョン指定を推奨している。また DVC の ML CI 解説は、コード変更ごとに data/model sanity check を自動化しつつ、重い学習や GPU 処理は schedule/manual に分離する方向を示している。

## Goals / Non-Goals

**Goals:**

- PR 必須の CPU CI をローカルで同じコマンドで再現できるようにする。
- GitHub Actions の quality / fast tests / slow tests を ML 向けに責務分離する。
- 失敗時の診断に必要なログと JUnit XML を artifact として必ず回収する。
- uv / Python / action version の取り扱いを最新の公式運用に揃える。

**Non-Goals:**

- 学習ロジックや loss 実装の変更
- self-hosted GPU runner 導入
- 外部 MLOps サービス連携の追加

## Decisions

- Decision 1: CI 実行コマンドは `scripts/ci_*.sh` に集約する。
  Rationale: workflow YAML に検証ロジックを分散させず、ローカル再現と CI を同一入口にできるため。

- Decision 2: GPU 専用 pytest には `pytest.mark.gpu` を付与し、CPU 向け suite は `not gpu` 条件を必須化する。
  Rationale: GPU 可視性に依存した skip 判定だけでは、GPU 搭載ローカル環境で CPU CI が再現できないため。

- Decision 3: required workflow では top-level `paths` filter を使わず、job 内で changed-files を解決して no-op / targeted 実行を分ける。
  Rationale: required check を path filter で skip すると、ブランチ保護下で pending 扱いになる運用リスクがあるため。

- Decision 4: workflow では `actions/checkout@v6`, `actions/setup-python@v6`, `astral-sh/setup-uv@v7`, `actions/upload-artifact@v7` を使用し、`setup-uv` の cache を有効化する。
  Rationale: 2026-03-28 時点の公式最新版系統であり、Node 24 対応・cache・problem matcher などの改善を取り込めるため。

- Decision 5: fast/slow pytest job は `tmp/github-actions/<suite>/` に JUnit XML とログを出力し、`if: always()` で artifact を保存する。
  Rationale: ML 統合テストは dependency やデータ処理由来の失敗解析が重いため、失敗後診断のコストを下げる必要がある。

- Decision 6: slow suite は CPU で成立する `slow and not gpu` に限定し、GPU 実機包括確認は既存 `scripts/test.sh` をローカル手順として維持する。
  Rationale: GitHub hosted runner で再現不能な GPU 学習を required check に混ぜない一方、研究用途の実機確認線は失わないため。

## Risks / Trade-offs

- [Risk] GPU marker の付与漏れがあると CPU CI に GPU 経路が混入する
  - Mitigation: 現在 GPU 条件を持つ test を明示的に網羅し、`pyproject.toml` に marker 登録を追加する。

- [Risk] changed-files 判定の shell 実装が空白を含むパスに弱い
  - Mitigation: repository では対象ファイルがほぼ空白なしであることを前提にしつつ、改行区切りから配列へ安全に取り込む bash 実装にする。

- [Risk] artifact 追加で workflow 実行時間と保存量が増える
  - Mitigation: retention を短めにし、JUnit とテキストログなど最小限に限定する。
