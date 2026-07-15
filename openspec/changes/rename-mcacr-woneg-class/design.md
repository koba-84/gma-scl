## Context

現在の公開クラス名 `MCACR_WONEG` はアンダースコアを含むため、全体のクラス命名ルールと整合しません。前 change では lint 例外として運用していたが、ユーザー要望により例外を撤廃し、同系統の命名ルールへ統一する。

## Goals / Non-Goals

**Goals:**
- `MCACR_WONEG` をアンダースコアなしの `MCACRWONEG` に改名する。
- 旧名の参照（import, Hydra `_target_`, テスト, 仕様）を全面更新する。
- Ruff の命名例外設定を削除する。

**Non-Goals:**
- Loss 数式や学習挙動の変更。
- 後方互換レイヤー（旧名エイリアス）の追加。

## Decisions

- 新クラス名は `MCACRWONEG` とする（要件どおり `_` を除去）。
- 旧名は残さず非互換移行とする（研究コード方針で後方互換を持たない）。
- 命名例外 requirement を削除し、規約は一律適用へ変更する。

## Risks / Trade-offs

- [Risk] 旧名依存コードの実行時エラー → Mitigation: リポジトリ内参照を網羅更新し、設定解決と pytest で回帰確認。
- [Risk] 外部利用者の旧 import 破壊 → Mitigation: change proposal に BREAKING を明記し、仕様と README で新名へ統一。
