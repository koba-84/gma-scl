## Context

`cfg_train` fixture は既定設定の `paths.data_dir=${paths.root_dir}/data` をそのまま使うため、`train(cfg_train)` を呼ぶテストが実データ `data/aapd/*.csv` を要求する。一方で CI runner には研究用 dataset を置いていないため `FileNotFoundError` で失敗する。workflow 側も changed files 取得に外部 action を使っており、PR コンテキストによってはトークン権限不足で 403 を返す。

## Goals / Non-Goals

**Goals:**
- train テストを synthetic dataset fixture だけで完結させる。
- code-quality workflow を GitHub 標準 checkout + git diff のみで完結させる。
- 変更は required checks の復旧に限定する。

**Non-Goals:**
- 学習ロジックそのものの変更
- dataset schema や tokenized pipeline の変更
- PR #1 全体の分割や履歴再構築

## Decisions

- Decision 1: `tests/conftest.py` に minimal CSV dataset 生成 helper を追加し、`cfg_train` fixture で毎回 `tmp_path` 配下へ書き出す。
  Rationale: train テストだけを hermetic 化でき、production data を repo に追加せずに済む。

- Decision 2: fixture 側で `paths.data_dir` と各 stage の `data_dir` / `dataset_name` / `num_classes` を synthetic dataset に合わせて上書きする。
  Rationale: Hydra 既定値を壊さず、train tests のみを self-contained にできる。

- Decision 3: `code-quality-pr.yaml` は `actions/checkout` の full fetch と `git diff --name-only` を使って変更ファイルを列挙する。
  Rationale: third-party changed-files action の permission 問題を避けつつ、既存の pre-commit 実行粒度を維持できる。

- Decision 4: `code-quality-pr.yaml` は `pre-commit/action` を使わず `uv sync --frozen` 後に `uv run pre-commit run --files ...` を直接実行する。
  Rationale: cache backend 障害や action 固有挙動を避け、ローカル運用と同じコマンドに揃える。

- Decision 5: interrogate hook は external hook env を使わず local system hook として `uv run interrogate` で実行する。
  Rationale: Python 3.12 isolated env の `pkg_resources` 欠落を回避し、ローカルと CI で同一の uv 環境を使えるため。

## Risks / Trade-offs

- [Risk] synthetic dataset の列数が config と不整合だと分類モデル生成が失敗する
  - Mitigation: fixture で `classification.data.num_classes` を dataset schema に合わせて明示的に上書きする。
- [Risk] workflow の git diff が空集合になるケース
  - Mitigation: 空なら pre-commit を skip する分岐を入れる。
- [Risk] CI セットアップ時間がやや増える
  - Mitigation: required checks の安定性を優先し、テスト workflow と同じ uv セットアップへ揃える。
