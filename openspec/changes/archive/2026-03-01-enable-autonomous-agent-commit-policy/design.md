## Context

現行仕様は commit 粒度やタイミングを定義しているが、coding agent がユーザーの追加指示なしで commit を実行できる条件が明文化されていない。結果として、実装完了後の運用が「毎回確認」か「黙示的自律実行」かで揺れる。

一次情報として、git は変更分離と小さな論理単位 commit を推奨し、GitHub は protected branch で直接 push 制御・required checks・required reviews を前提にしている。さらに GitHub Copilot coding agent は PR ベースの人間レビュー前提運用であり、自律実行を許可しても最終統合はレビューゲート配下に置く設計が妥当である。

## Goals / Non-Goals

**Goals:**

- coding agent が自律 commit してよい条件を仕様として機械判定可能にする。
- commit 前の必須品質ゲートを明確化し、再現性を維持する。
- branch 保護・レビュー前提に整合する禁止事項を追加する。

**Non-Goals:**

- CI/CD や GitHub Branch Protection 設定そのものの自動変更。
- merge 実行ポリシーの自動化。
- commit message 形式要件の変更。

## Decisions

- Decision 1: 自律 commit の実行条件を agent-operation-policy に追加する。

  - Rationale: agent 振る舞いの主仕様が同ファイルであり、実行可否を直接定義できる。
  - Alternative: version-control のみで規定。却下理由: 「誰が実行するか」が曖昧なまま残る。

- Decision 2: Python 変更を含む自律 commit では `uv run pre-commit run -a` 成功を必須化し、失敗時は commit 禁止にする。

  - Rationale: 既存の dev-quality-tooling 要件と一致し、判定が明確。
  - Alternative: fast test のみ必須化。却下理由: lint/type 品質ゲートを迂回してしまう。

- Decision 3: agent は protected branch への直接 push/merge を行わず、review 前提の commit 境界提示までを責務とする。

  - Rationale: GitHub の保護ブランチ運用・Copilot coding agent の PR ワークフローと整合。
  - Alternative: agent に merge まで許可。却下理由: レビュー統制を崩す。

## Risks / Trade-offs

- [Risk] 自律 commit 条件を厳格化しすぎると作業速度が低下する。→ Mitigation: 必須は pre-commit 成功に限定し、`pytest -m "not slow"` は推奨のまま維持する。
- [Risk] ローカル dirty tree 混在で自律 commit が頻繁に停止する。→ Mitigation: 対象外差分混在時の停止条件を明示し、ユーザー判断へ委譲する。
