## 1. Agent Commit Policy

- [x] 1.1 `openspec/specs/agent-operation-policy/spec.md` に自律 commit 実行条件と禁止条件を反映する
- [x] 1.2 対象外差分混在時の commit 停止条件を現行要件と矛盾しない形で統合する

## 2. Quality Gate Sync

- [x] 2.1 `openspec/specs/dev-quality-tooling/spec.md` に「自律 commit 前の pre-commit 成功必須」を反映する
- [x] 2.2 Python 変更時の mypy フック必須を自律 commit 要件として明記する

## 3. Version Control Guidance

- [x] 3.1 `openspec/specs/version-control.md` に自律 commit の運用条件を追記する
- [x] 3.2 仕様根拠に一次情報 URL（git-scm / docs.github.com）を追加する

## 4. Validation

- [x] 4.1 OpenSpec change artifact（proposal/design/specs/tasks）が完了状態であることを確認する
- [x] 4.2 変更後仕様の整合（agent-operation-policy, dev-quality-tooling, version-control）を確認する
