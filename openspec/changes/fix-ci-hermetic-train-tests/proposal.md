## Why

PR #1 の GitHub Actions で `fast_tests` と `code-quality` が失敗しており、required checks を満たせず merge できない。`tests/train.py` は実データ `data/aapd/train.csv` に依存しており CI 上で hermetic ではない。加えて `code-quality` workflow は `trilom/file-changes-action` の権限不足で `Resource not accessible by integration` を起こしている。

## What Changes

- train テスト用の Hydra fixture を synthetic CSV dataset に差し替え、CI 上でも self-contained に実行できるようにする。
- Code Quality PR workflow から permission-sensitive な changed-files action を除去し、git diff ベースで変更ファイルを求める。
- Code Quality PR workflow では `pre-commit/action` を使わず、uv 環境で `pre-commit run` を直接実行する。
- interrogate hook は isolated pre-commit env ではなく project の uv 環境で実行する。
- 上記の回帰を防ぐため、targeted pytest と pre-commit で検証する。

## Capabilities

### Modified Capabilities

- `training`: train テストは実データを前提にせず synthetic dataset で成立する。
- `dev-quality-tooling`: PR 向け code-quality workflow は GitHub App 権限不足で失敗しない。

## Impact

- 影響コード: `tests/conftest.py`, `.github/workflows/code-quality-pr.yaml`
- 外部 API 影響: なし
- CI 影響: GitHub Actions の required checks が再び再現可能になる
