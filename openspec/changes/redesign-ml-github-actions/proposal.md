## Why

現在の GitHub Actions は quality/test job ごとに依存解決や実行条件が分散しており、ML リポジトリとして重要な「CPU 上で再現できる必須チェック」と「GPU や長時間を要する確認」の責務分離が不明確である。特に `uv run pytest -m "not slow"` は GPU が見えるローカル環境では GPU テストまで拾うため、PR 用 CPU CI の再現コマンドとして成立していない。

## What Changes

- GitHub Actions 用の ML CI 仕様を新設し、required PR checks、scheduled/manual slow checks、cache、artifact、concurrency、permissions の基準を定義する。
- code-quality と pytest 実行を repository 内の共通スクリプトへ集約し、ローカル再現コマンドと Actions 実行コマンドを一致させる。
- GPU 専用 pytest を明示マーカー化し、CPU CI の fast/slow suite から除外する。
- required workflow では top-level path filter に依存せず、checkout 後の git metadata に基づく changed-files 判定で no-op を許容する。
- 失敗時診断のため、pytest の JUnit XML と workflow ログを artifact として保存する。

## Capabilities

### New Capabilities

- `ml-ci-workflows`: ML プロジェクト向け GitHub Actions の責務分離、実行条件、診断情報保存を規定する

### Modified Capabilities

- `dev-quality-tooling`: code-quality workflow は repository 提供の uv ベース検証コマンドを使い、ローカル品質ゲートと一致させる
- `training`: CPU CI 用 pytest suite は GPU マーカーを除外し、GPU 検証はローカル実機確認へ分離する

## Impact

- 影響コード: `.github/workflows/*.yml`, `pyproject.toml`, `tests/train.py`, `scripts/*.sh`, `README.md`
- 外部依存: GitHub Actions 公式 action と `astral-sh/setup-uv`
- ローカル検証: `uv run pre-commit run -a` と CPU pytest suite の再現性向上、GPU 検証は `scripts/test.sh` を継続
