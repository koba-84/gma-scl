## ADDED Requirements

### Requirement: Atomic commit granularity for reproducible changes

開発者は MUST 1 commit を単一の論理変更に限定し、変更追跡と再現調査が可能な履歴を維持しなければならない。

#### Scenario: Split unrelated edits into separate commits

- **WHEN** 開発者が機能変更とリネームまたは整形を同時に行った
- **THEN** 機能変更と無関係編集は別 commit に分割される

#### Scenario: Validate each commit baseline

- **WHEN** 開発者が commit を作成する
- **THEN** 少なくとも設定解決または該当 fast テストがその commit 単体で成立する

### Requirement: Topic-scoped push granularity with pre-push gate

開発者は MUST push を同一トピック change の commit 群に限定し、push 前に fast テストを通過させなければならない。

#### Scenario: Push only coherent topic commits

- **WHEN** 開発者がリモートへ push する
- **THEN** push される commit 群は単一トピックに限定され、未整理の暫定 commit を含まない

#### Scenario: Run fast checks before push

- **WHEN** 開発者が PR/push 前最終確認を行う
- **THEN** `uv run pytest -m "not slow"` が成功している
