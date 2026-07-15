## Context

gitworkflows は変更を separate changes として分けることを推奨しているが、commit 数の具体的な上限は示していない。GitHub Docs も squash merge により WIP commit を default branch の履歴へ残さず、rebase merge で線形履歴を保てると説明している。一方で GitLab Docs は squash and merge が clean history と meaningful commit を作ると説明している。つまり一次資料が支持しているのは「小さく意味のある論理単位」「線形履歴」「merge 時の squash/rebase 活用」であり、固定の commit 数 30 ではない。

## Goals / Non-Goals

**Goals**

- 根拠の薄い固定数値を必須仕様から外す。
- 一次資料で裏付けられる履歴整理原則だけを hard requirement として残す。
- 必要なチームだけが `BRANCH_HISTORY_MAX_COMMITS` を任意 override として使えるようにする。

**Non-Goals**

- 既存の merged history を rewrite すること。
- PR size を行数ベースで新たに強制すること。

## Decisions

1. `BRANCH_HISTORY_MAX_COMMITS` の既定値は削除する。
- 理由: 一次資料に commit 数の汎用上限は見当たらず、既定 hard gate にすると仕様の根拠が弱い。

2. hard requirement は `merge commit なし` と `protected branch への直接 push 禁止` を維持する。
- 理由: これらは GitHub merge method / protected branch の一次資料、および git-rebase の線形履歴運用と整合する。

3. commit 数制限は任意 override に格下げする。
- 理由: チーム局所の運用値としては有用だが、source-backed な universal rule ではない。

## Risks / Trade-offs

- [Risk] 既定の件数 gate を外すと長い topic branch を機械的には止めにくくなる
  - Mitigation: 仕様本文で squash/rebase merge と small/focused reviewable changes を明記する。
- [Risk] チームごとの好みが分かれる
  - Mitigation: `BRANCH_HISTORY_MAX_COMMITS` を任意 override として残す。

## Migration Plan

1. OpenSpec delta で version-control requirement を更新する。
2. `scripts/validate_branch_policy.sh` を既定無効の optional threshold に変更する。
3. pre-commit と対象 shell script 検証を実行する。
