## Context

現在の loss 実装では aggregation helper が `src/models/loss/aggregation.py` と `src/models/loss/components/aggregation.py` に分かれており、MCACR と MXCLR が別々のモジュール契約に依存しています。さらに MCACR が train.csv 由来の統計計算まで抱えており、label statistics の責務境界が曖昧です。

transport helper も family ごとに公開関数を分けていますが、入力契約は共通で、差分は mass 正規化と solver 種別だけです。公開面を 1 つに寄せたほうが呼び出し経路を追いやすくなります。

## Goals / Non-Goals

**Goals:**
- 未使用関数検出を再現可能な dev tooling として導入する
- loss helper の配置を `components` 配下に統一する
- MCACR の label statistics 計算を loss 本体から分離する
- MXCLR transport の公開 API を 1 つに絞る

**Non-Goals:**
- loss の数式や学習挙動を変えない
- 旧 import path を保つ互換レイヤーを追加しない
- vulture を pre-commit の必須フックへ追加しない

## Decisions

- `pyproject.toml` の dev group に vulture を追加し、`tool.vulture` で scan path と除外対象を管理する
  - 代替案として ad-hoc に CLI 引数だけで運用する案もあるが、再現性が低いため採用しない
- MCACR が使う train.csv 由来の count / NPMI / frequency helper は `src/models/loss/components/label_stats.py` に移す
  - 既存の `components` 契約と整合し、MXCLR との共有もしやすいため
- `src/models/loss/aggregation.py` は削除し、MCACR も `components/aggregation.py` の canonical helper に統一する
  - 代替案として top-level を残す案は、重複を温存するだけなので採用しない
- transport の公開関数は strategy 引数を持つ 1 つの helper にまとめる
  - 代替案として wrapper を残す案は、呼び出し箇所を減らせないため採用しない

## Risks / Trade-offs

- [Risk] vulture の機械判定で false positive を削除する可能性 → Mitigation: 100% confidence を起点にし、grep で実参照も確認する
- [Risk] helper 移設で import 更新漏れが起きる可能性 → Mitigation: ruff/mypy/pre-commit と対象 self-test で検証する
- [Risk] transport helper 統合で mass 正規化条件を崩す可能性 → Mitigation: 既存 family ごとの差分を enum/文字列分岐として明示し、MXCLR property test と config resolve で確認する

## Migration Plan

- topic branch 上で OpenSpec change を作成する
- task ごとに検証付きでコミットする
- main spec へ同期後に change を archive する
- PR を作成し、CI 通過後に merge して main に戻す

## Open Questions

- なし
