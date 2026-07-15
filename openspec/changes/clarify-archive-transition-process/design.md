## Context

現行の version-control 仕様は commit/push 粒度を主に扱っており、OpenSpec change 完了後の archive 移行条件が明確でない。そのため、完了済み change が作業中ディレクトリに残る。

## Goals / Non-Goals

**Goals:**

- archive 前提条件を最小で明確化する（完了済みのみ移行可）。
- archive 先命名と移行後の成立条件を定義する。

**Non-Goals:**

- OpenSpec CLI 本体の実装変更。
- 既存 archive ディレクトリのリネームや再整理。
- spec 同期可否の判断基準追加。

## Decisions

1. archive 運用は `version-control` capability に requirement 追加で管理する。
   理由: 既存の開発運用規約と同一ドキュメントで一貫管理できる。

2. archive 実行条件は「`openspec status --change <name>` が complete であり、tasks に未完了がないこと」に限定する。
   理由: 最小運用で完了判定を揃えられる。

3. archive 名は `YYYY-MM-DD-<change-name>` に固定し、同名がある場合は停止する。
   理由: 時系列追跡を維持しつつ上書き事故を防ぐ。

4. archive 後は active 側に change が残らず、archive 側に同 change が存在する状態を成立条件とする。
   理由: 状態が一意に判定できる。

## Risks / Trade-offs

- [Risk] 同期判断を人手に依存すると漏れが起きる。
  Mitigation: 本 change では同期判断を要件化しない（別 change で扱う）。
- [Risk] strict 化により archive 作業が増える。
  Mitigation: 要件を完了確認・移動・移行後確認の 3 点に限定する。
