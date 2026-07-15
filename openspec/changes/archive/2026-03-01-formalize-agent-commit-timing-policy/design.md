## Context

現行仕様には commit の粒度はあるが、commit を作るタイミングと、dirty tree を検出した際の agent の必須動作が不足している。結果として、作業単位は明確でも「いつ commit するか」「既存差分があるときにどう進めるか」が実装者依存になる。

外部根拠として、git 公式は小さく論理的に分離された変更履歴を推奨しており、GitHub 公式は pull request を小さく焦点化することを推奨している。加えて GitHub Copilot coding agent は agent 生成変更を人間レビュー前提で扱う運用を示しているため、ローカル側でも change 単位の境界管理を必須化する必要がある。

## Goals / Non-Goals

**Goals:**

- commit タイミングを MUST ルールとして定義する。
- dirty tree 開始時の agent 動作を仕様化し、混在コミットを防止する。
- pre-commit と mypy を commit 直前ゲートとして統一する。
- OpenSpec change 単位での実装完了条件（spec/tasks/検証/commit）を明示する。

**Non-Goals:**

- ブランチ戦略（GitHub Flow / trunk-based）の強制。
- 既存の未コミット変更を自動的に再構成する仕組みの導入。
- CI の必須化（個人開発で pre-commit 中心運用を継続）。

## Decisions

- `version-control` 仕様を更新し、commit 実行タイミングを 3 条件で定義する。
  - 条件1: 単一論理変更が完了した時点。
  - 条件2: その変更に対応する必須検証（pre-commit 等）が成功した時点。
  - 条件3: 他トピック差分が commit に混在しない時点。
- `version-control` に dirty tree 開始時の必須手順を追加する。
  - agent は作業開始時に `git status --short` を確認する。
  - 対象外差分がある場合は、その差分を commit に混ぜない。
  - 混在回避不能なら作業を停止し、ユーザー確認を要求する。
- `dev-quality-tooling` 仕様を更新し、commit 直前ゲートとして以下を固定する。
  - `uv run pre-commit run -a` の成功を MUST。
  - Python 変更を含む commit では mypy hook 成功を MUST。
- `agent-operation-policy` を新設し、OpenSpec change 駆動の完了定義を追加する。
  - proposal/spec/design/tasks の整合。
  - 実装差分の検証完了。
  - 論理単位 commit の作成。
  - push 可否の判定結果を報告に明記。

代替案として「push 前のみ検証」を検討したが、失敗差分がローカルで長期滞留しやすくなるため不採用。

## Risks / Trade-offs

- [Risk] commit 前検証の回数増加で作業テンポが落ちる → Mitigation: 変更範囲に応じた最小検証セットを tasks.md に先に定義する。
- [Risk] dirty tree が常態化した環境で作業が止まりやすい → Mitigation: agent-operation-policy に「対象外差分を触らない」原則を固定し、停止条件を明確化する。
- [Risk] 文書規約が増えて運用が複雑化する → Mitigation: OpenSpec spec に集約し README から参照できるようにする。
