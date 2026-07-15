## Context

本リポジトリは研究用途のため、命名の揺れがあるとレビュー時の解釈差や設定参照ミスが再現性リスクになります。現状は loss 実装と pytest ファイル命名のみ部分規約があり、関数・クラス・変数・モジュール名の全体規約が欠けています。加えて、Ruff では pep8-naming（N ルール）を未有効化のため、命名逸脱を機械的に検知できません。

外部調査では、Python 命名は PEP 8 を基準に snake_case / CapWords / UPPER_CASE を使い分けること、公開 API 名は利用者向け一貫性を優先することが示されています。ML コード運用上は、モデル/損失クラス名の安定性とファイル名の対応関係を固定することで実験設定の可読性が向上します。

## Goals / Non-Goals

**Goals:**
- 関数・クラス・変数・定数・ファイル名の統一ルールを OpenSpec に新設する。
- 既存の品質ゲートに命名検証を組み込み、commit 前に自動ブロックする。
- 既存命名例外を最小化し、残す場合は理由を仕様と設定に明記する。
- training 仕様の公開 loss クラス一覧に `MXCLR` を追加し、仕様と実装の乖離を解消する。

**Non-Goals:**
- Python 以外（YAML キー名、ログ名、W&B run 名など）の命名規約追加。
- 大規模な API 再設計。
- 既存研究結果に影響するアルゴリズム変更。

## Decisions

1. 基準規約として PEP 8 準拠の命名を採用する。
- 関数/メソッド/モジュール/変数: snake_case
- クラス/例外: CapWords
- 定数: UPPER_CASE
- 非公開属性: 先頭アンダースコア
- 理由: Python 標準規約であり、外部貢献者にとって認知負荷が最小。

2. 機械的検証は Ruff の pep8-naming（N）で実施する。
- `tool.ruff.lint.select` に `N` を追加し、pre-commit の既存 Ruff フックで強制する。
- 理由: 既存運用に自然統合でき、追加ツール導入なしで即時適用可能。

3. ドメイン制約で残す命名は例外として明示する。
- `MCACR_WONEG` は論文・既存設定ファイルとの対応維持のため、`ignore-names` に明示する。
- その他の一般的逸脱（`RunIf`, `as F`, `as L`）は修正して例外化しない。
- 理由: 例外は最小化しつつ、研究コンテキストの可読性は維持する。

4. loss 公開クラス命名仕様は training capability に追記する。
- 既存列挙（Base/MulSupCon/MCACR_WONEG/MSC）へ `MXCLR` を追加する。
- 理由: 実装には存在するため、仕様漏れのみを補正する。

## Risks / Trade-offs

- [Risk] 命名変更により import パス参照が壊れる → Mitigation: 参照箇所を同時修正し、`uv run pre-commit run -a` と `uv run pytest -m "not slow"` で回帰確認。
- [Risk] 例外の過剰追加で規約が形骸化する → Mitigation: 例外は `MCACR_WONEG` のみ許容し、仕様に理由を固定する。
- [Risk] 研究コミュニティ慣習（例: `F` エイリアス）との乖離 → Mitigation: 可読性優先で `functional` へ統一し、ドキュメントに明記。
