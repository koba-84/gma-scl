## Context

`uv run pre-commit run -a` は Python 品質ゲートとして必須だが、同時に Markdown 整形系フック（`trailing-whitespace`、`end-of-file-fixer`、`mdformat`）が動作し、作業対象外の Markdown 差分を生成することがある。これにより OpenSpec の 1 タスク 1 コミット制約で、タスクに無関係な差分混入リスクが高まっている。

本 change では、フック責務の境界と差分発生時の標準運用を `dev-quality-tooling` 仕様へ明記し、再現性とコミット粒度を両立させる。

## Goals / Non-Goals

**Goals:**

- Markdown 自動修正が起きる条件をフック単位で説明可能にする。
- 自動修正差分が発生したときの標準運用（保持、分離、作業継続）を仕様化する。
- Python タスクの検証手順と、Markdown 差分処理の順序を明確化する。

**Non-Goals:**

- pre-commit フックの無効化や除外設定の追加。
- Markdown 整形ポリシー自体の変更。
- 既存のコミットメッセージ規約や version-control 仕様の改訂。

## Decisions

### Decision 1: 仕様更新は `dev-quality-tooling` に限定する

- 理由: 本件は実装コード変更ではなく、pre-commit 運用ルールの明確化が目的のため。
- 代替案: `version-control` へ追記。
- 不採用理由: commit 粒度の一般規約と、pre-commit 固有運用の責務が混在し可読性が下がる。

### Decision 2: 差分混入時は「対象外差分を先に分離」する手順を標準化する

- 理由: 1 タスク 1 コミットを維持しつつ、pre-commit 検証失敗ループを避けられるため。
- 代替案: そのまま同一コミットへ含める。
- 不採用理由: OpenSpec タスク完了定義（対象ファイル限定コミット）に反する。

### Decision 3: 原因特定はフック単位の実行ログで行う

- 理由: `pre-commit run -a` 一括実行だけでは、どのフックが Markdown を変更したか追跡しづらい。
- 代替案: 結果差分のみを確認。
- 不採用理由: 原因と運用判断の根拠が曖昧になる。

### Decision 4: Markdown 関連フックの責務境界を固定して扱う

- `trailing-whitespace`: 末尾空白の除去を行い、`types` 未指定のため Markdown を含むテキスト系ファイルへ適用される。
- `end-of-file-fixer`: 末尾改行を正規化し、`types` 未指定のため Markdown を含むファイルへ適用される。
- `mdformat`: Markdown 構文整形を行い、Markdown ファイルに限定して適用される。
- 実行条件: いずれも `uv run pre-commit run -a` 時は全対象ファイルに対して実行される。

この責務境界を基準に、Markdown 差分が発生した際の原因フック特定と差分分離判断を行う。

## Risks / Trade-offs

- [Risk] 手順が増え、開発者の即時負荷が上がる → Mitigation: 仕様に最小コマンド列を提示し、判断分岐を固定化する。
- [Risk] 「対象外差分」の判定が人依存になる → Mitigation: 対象タスクに含まれるファイル範囲を tasks と commit メッセージで明示する。
- [Risk] 既存の未整理差分がある状態では運用が適用しづらい → Mitigation: 作業開始時の `git status --short` 確認を必須手順として再確認する。

## Migration Plan

1. `openspec/changes/prevent-precommit-markdown-autorewrite/specs/dev-quality-tooling/spec.md` を追加し、要件とシナリオを定義する。
2. 仕様に沿って `tasks.md` で実施手順を分解する。
3. 実装段階では docs と運用手順の変更のみを対象にし、Python コード変更は行わない。
4. `uv run pre-commit run -a` と必要最小限のテストで整合性を確認する。

## Open Questions

- Markdown 差分を分離する際、同一 change 内の別タスクとして扱うか、別 change として扱うかの境界をどこに置くか。
- `mdformat` 由来差分と `trailing-whitespace` 由来差分が同時に出た場合の推奨優先順位を仕様で固定するか。

## Validation Snapshot

- Command: `uv run openspec validate prevent-precommit-markdown-autorewrite --strict`
- Result: `Change 'prevent-precommit-markdown-autorewrite' is valid`

## Operational Assumptions

- Python タスク commit 前に `uv run pre-commit run -a` を実行する運用は継続する。
- 自動修正が対象外 Markdown に及んだ場合、対象タスク commit へ混在させず分離する。
- 差分分離後は同一作業ツリーで `uv run pre-commit run -a` を再実行し、成功状態を確認する。
