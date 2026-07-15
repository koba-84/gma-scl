# 未コミット差分の整理手順（2026-03-01）

## 目的

現時点の混在差分を OpenSpec change 単位で分離し、単一論理変更ごとに commit できる状態へ整理する。

## 前提ルール

- 作業開始時に git status --short を確認する。
- 1 commit は 1 change 相当の論理変更だけを含める。
- 各 commit の直前に uv run pre-commit run -a を実行し、成功した変更だけを commit する。
- push は同一トピックの commit 群単位で行う。

## 現在の差分分類

### グループA: wandb failure state 修正

候補ファイル:

- src/utils/utils.py
- src/train.py
- tests/test_task_wrapper.py
- openspec/changes/fix-wandb-failure-state/

対応 change:

- fix-wandb-failure-state

### グループB: MSC prototype ルーティング整合

候補ファイル:

- src/models/loss/msc.py
- configs/contrastive/model/msc.yaml
- src/train.py
- openspec/changes/align-msc-prototype-routing-with-supcon/

対応 change:

- align-msc-prototype-routing-with-supcon

### グループC: MCACR / MXCLR 集約方式（agg）

候補ファイル:

- src/models/loss/mxclr.py
- configs/contrastive/model/mxclr.yaml
- configs/contrastive/model/mcacr.yaml
- src/models/loss/__init__.py
- openspec/changes/add-mcacr-agg-branch/
- openspec/changes/add-mxclr-agg-branch/
- openspec/changes/unify-aggregation-spec-contract/

対応 change:

- add-mcacr-agg-branch
- add-mxclr-agg-branch
- unify-aggregation-spec-contract

### グループD: 開発基盤（uv/ruff/mypy）と文書更新

候補ファイル:

- README.md
- openspec/project.md
- scripts/build_aapd_arxiv_label_descriptions.py
- scripts/build_npmi.py
- scripts/preprocess.py
- uv.lock
- openspec/changes/standardize-uv-add-installation-docs/
- openspec/changes/add-ruff-dev-tooling/

対応 change:

- standardize-uv-add-installation-docs
- add-ruff-dev-tooling

### グループE: 探索/一時物の整理

候補ファイル:

- REPORT_tmp.html (delete)
- notebooks/.gitkeep (delete)
- wandb/ (untracked)

扱い:

- 研究成果に不要なら削除コミットを独立作成。
- 生成物なら .gitignore 方針を先に確定してから反映。

## 実行順序（推奨）

1. グループAを分離して commit
2. グループBを分離して commit
3. グループCを分離して commit
4. グループDを分離して commit
5. グループEを最後に整理

## 実行テンプレート

以下を各グループで繰り返す。

1. 対象だけ stage

- git add <group-files>

2. 差分確認

- git diff --cached --name-only
- git diff --cached

3. 検証

- uv run pre-commit run -a

4. commit

- git commit -m "<Verb>: <topic>"

5. 残差確認

- git status --short

## 注意点

- src/train.py は複数グループで競合しやすい。先に A/B のどちらへ属する変更かを split してから stage する。
- uv.lock は依存変更の commit にのみ含める。
- 未分類差分が残る場合は commit せず、次グループへ持ち越さずに再分類する。
