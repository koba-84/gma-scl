## Why

現在の仕様は commit 粒度は定義されている一方で、commit をいつ作るべきか、既存の未コミット変更がある状態で agent がどう振る舞うべきかが曖昧です。OpenSpec・Git・GitHub Coding Agent の公式ガイダンスに合わせ、実行タイミングと作業境界を明文化して運用ぶれをなくす必要があります。

## What Changes

- Git 運用仕様に「commit 実行タイミング」の MUST ルールを追加する。
- 既存の未コミット変更がある場合の agent 作業開始条件と、混在時の扱いを明文化する。
- pre-commit をローカル品質ゲートとする運用に加え、commit 前に必ず対象範囲の検証が完了していることを明記する。
- OpenSpec change 単位での実装・検証・commit 完了までの作業フローを agent 運用仕様として新設する。

## Capabilities

### New Capabilities

- agent-operation-policy: coding agent が OpenSpec change に従って作業を切り分け、未コミット混在時の扱い、commit/push 実行条件、報告内容を一貫運用する。

### Modified Capabilities

- version-control: commit 粒度に加えて commit タイミングと dirty tree 開始時の扱いを要件化する。
- dev-quality-tooling: pre-commit と mypy を commit 直前ゲートとして運用する条件を明確化する。

## Impact

- 影響仕様:
  - openspec/specs/version-control.md
  - openspec/specs/dev-quality-tooling/spec.md
  - openspec/specs/agent-operation-policy/spec.md（新規）
- 影響運用:
  - 作業開始時のブロッカー判定、commit 実行タイミング、報告内容が統一される
