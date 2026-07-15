# Git 変更管理仕様（Version Control Spec）

## Purpose

本仕様は、研究コードの再現性を維持するために git commit と push の粒度と事前検証を規定する。

## 1. commit 粒度（必須）

- 1 commit は単一の論理変更のみを含むこと。
- 機能変更と無関係な整形、リネーム、ドキュメント整理は別 commit に分離すること。
- 各 commit は、その commit 単体で変更意図を説明できること。
- 各 commit は、少なくとも設定解決または該当 fast テストが成立する状態で作成すること。

## 2. push 粒度（必須）

- 1 push は同一トピック（同一 OpenSpec change）に属する commit 群に限定すること。
- 未整理の暫定 commit を含めたまま push しないこと。
- push 先は topic branch を基本とし、`main` `dev` `release/*` への直接 push を行わないこと。
- push 前に `uv run pre-commit run -a` を実行し、成功させること。
- `uv run pytest -m "not slow"` は追加検証として推奨するが必須ではない。

## 3. commit タイミング（必須）

- commit は「単一論理変更が完了し、必要な検証が成功した時点」で作成すること。
- Python 変更を含む commit は、`uv run pre-commit run -a` 成功後に作成すること。
- Python 変更を含む commit は、mypy フック成功後に作成すること。
- 未完了の別トピック変更が混在した状態で commit を作成しないこと。
- commit message は `openspec/specs/commit-message-policy/spec.md` の要件に準拠すること。
- commit message の言語運用は、件名 Type と必須見出し（Why/Validation/Reproducibility）を英語固定とし、各見出し配下の説明は日本語または英語を許容すること。
- coding agent は上記条件を満たした場合、追加のユーザー明示指示なしで自律的に commit を作成すること。
- coding agent は上記条件を満たさない場合、commit を作成せず停止理由を報告すること。

## 4. dirty tree 開始時の取り扱い（必須）

- coding agent は作業開始時に `git status --short` を確認すること。
- 対象外の未コミット差分がある場合、対象外差分を編集・revert・commit しないこと。
- 対象差分との混在回避が困難な場合、作業を停止してユーザーに確認すること。

## 5. OpenSpec change archive 移行（必須）

- 開発者および coding agent は、完了済み OpenSpec change のみを archive へ移行すること。
- 開発者および coding agent は、完了条件確認後に追加指示を待たず自律的に archive を実行すること。
- archive 前に `openspec status --change <name>` が complete であることを確認すること。
- archive 前に `openspec/changes/<name>/tasks.md` のチェックボックスに未完了がないことを確認すること。
- archive 先は `openspec/changes/archive/YYYY-MM-DD-<change-name>` 命名規約を使用すること。
- archive 先に同名パスが存在する場合は上書きせずに処理を停止すること。
- archive 後は active 側 `openspec/changes/<name>` が存在しないこと、archive 側に対象ディレクトリが存在することを確認すること。
- 対象外差分混在などで安全に archive 実行できない場合は実行を中断し、停止理由と必要な次アクションを報告すること。

確認コマンド例:

- 完了確認: `uv run openspec status --change <name> --json`
- tasks 未完了確認: `grep -n "^- \\[ \\]" openspec/changes/<name>/tasks.md`
- archive 実行後確認:
  - `test ! -d openspec/changes/<name>`
  - `test -d openspec/changes/archive/YYYY-MM-DD-<change-name>`

## 6. commit メッセージ（推奨）

- 先頭を動詞（Add/Fix/Refactor/Docs/Test/Chore）で開始する。
- 1 行目に変更主題を簡潔に記述する。
- 必要な場合のみ本文に実行コマンドと結果要約を記録する。

## 7. topic branch 履歴整理（必須）

- push 前の outgoing history は線形（merge commit なし）であること。
- push 前の outgoing history は review 可能な論理単位で構成されていること。
- `BRANCH_HISTORY_MAX_COMMITS` を明示設定した場合のみ、outgoing history の commit 数上限を追加で適用してよい。
- upstream 未設定時は `BRANCH_HISTORY_BASE_REF`（未指定時 `origin/main`）を比較基準に使うこと。
- 上記検証は `scripts/validate_branch_policy.sh` の pre-push で自動実行すること。
- work-in-progress commit は squash merge または merge 前の interactive rebase / autosquash で整理し、default branch には意味のある commit のみを残すこと。
- 緊急時の一時回避は `BRANCH_POLICY_BYPASS=1` の明示設定時のみ許可すること。

確認コマンド例:

- outgoing merge commit 数: `git rev-list --count --merges "$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || echo origin/main)..HEAD"`
- optional outgoing commit 数確認: `git rev-list --count "$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || echo origin/main)..HEAD"`
- autosquash 実行例: `git rebase -i --autosquash <base-ref>`

## 8. 根拠

- git 公式 user-manual において、patch は単一の論理変更で構成する方針が示されている。
- gitworkflows でも変更分離（separate changes）が推奨されている。
- git-rebase は interactive rebase / autosquash による commit 整理を提供している。
- GitHub Docs の merge methods は squash merge により WIP commit を統合して clear history を作り、rebase merge により線形履歴を維持できると説明している。
- GitLab Docs の squash and merge も、小さな commit を単一の meaningful commit にまとめると history が clean になり revert しやすいと説明している。
- GitHub Docs の protected branches は、required status checks と required reviews を通じた統制前提を示している。
- GitHub Copilot coding agent は agent 生成変更を人間レビュー前提で扱う運用を示している。
- 一次資料は具体的な commit 数上限までは規定していないため、固定数値の hard default は採用せず、件数 cap が必要な場合だけ `BRANCH_HISTORY_MAX_COMMITS` を明示設定する。
- 本リポジトリでは同一 commit と同一設定での再現を重視しているため、上記方針を commit/push 運用規約として採用する。

参考 URL:

- https://git-scm.com/docs/user-manual#_making_a_change
- https://git-scm.com/docs/gitworkflows
- https://git-scm.com/docs/git-rebase
- https://docs.github.com/en/get-started/using-git/about-git
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github
- https://docs.gitlab.com/user/project/merge_requests/squash_and_merge/
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/about-copilot-coding-agent
