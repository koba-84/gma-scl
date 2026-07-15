## Context

configs/hparams_search は試行的な探索設定を置くディレクトリであり、恒久仕様として管理すべき対象ではない。一方で、過去の運用では一部ファイルが追跡され、PRに不要差分が混入していた。運用の明確化と差分ノイズ削減のため、追跡停止と仕様上の扱いの明文化を同時に行う。

## Goals / Non-Goals

**Goals**

- configs/hparams_search 配下をGit追跡対象外にする。
- 既存追跡ファイルを安全に追跡解除する。
- 当該ディレクトリ編集を仕様変更の根拠にしない運用ルールをOpenSpecへ追加する。

**Non-Goals**

- 既存の main ブランチ履歴全体を書き換える強制運用をこの変更で実施すること。
- hparams_search 配下ファイル内容の最適化や再設計。

## Decisions

1. ignore は個別ファイル指定ではなくディレクトリ単位で設定する。
- 理由: 一時探索ファイルが増減しても追跡漏れ/残存を防げるため。

2. 追跡解除は git rm --cached で実施し、ワーキングツリー上の実ファイルは保持する。
- 理由: 実験継続に必要なローカル設定を失わないため。

3. OpenSpec は agent-operation-policy を更新し、configs/hparams_search 編集は仕様変更の入力にしない要件を追加する。
- 理由: 運用意図を仕様として残し、後続作業での誤用を防ぐため。

## Risks / Trade-offs

- [Risk] 既存履歴に残る過去コミットまでは通常PRで消せない
  - Mitigation: この変更では追跡解除と今後の再発防止を担保し、全履歴削除が必要な場合は別途 force-push 前提の履歴改変手順を計画する。

- [Risk] ignore 後に必要な共有設定までローカル化される可能性
  - Mitigation: 共有すべき設定は configs/hparams_search 以外の管理対象ディレクトリへ移す方針を明記する。

## Migration Plan

1. OpenSpec artifacts（proposal/specs/tasks）を作成する。
2. .gitignore とインデックス追跡を更新する。
3. pre-commit を実行し、変更をコミットする。
4. PR作成後にCI通過を確認し、mergeする。
