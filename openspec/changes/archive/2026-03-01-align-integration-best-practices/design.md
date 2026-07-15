## Context

Transformers の testing ガイドでは、fast/slow を分離し fast を常時回す運用が推奨される。TFDV ではデータ異常や skew/drift の早期検知を重視し、Google の ML テスト指針では再現性とデータ品質検証が重要項目である。現状は学習経路の統合はあるが、fast integration の観点で data quality/reproducibility が薄い。

## Goals / Non-Goals

**Goals:**

- fast integration に data quality（簡易 skew）検証を追加する。
- fast integration に再現性（seed 固定）検証を追加する。
- tests 配下のファイル名から `test` 語を除去して統一する。

**Non-Goals:**

- 本番監視レベルの drift 検知機構を実装すること。
- slow/GPU テストを fast 側に移すこと。

## Decisions

1. data quality は tiny CSV でのラベル比率 skew を統合テストで検証する。
   理由: 低コストでデータ破損系の回帰を検知できるため。

2. reproducibility は `ContrastiveDataModule` の DPP 経路で固定 seed + 同一埋め込みの batch 一致を検証する。
   理由: 現行実装に即した再現性チェックとして有効なため。

3. ファイル命名は機能名ベース（例: `train.py`, `data_integration.py`）に統一し、`test` 語を使わない。
   理由: tests ディレクトリ配下での冗長性を下げ、命名規約を単純化するため。

## Risks / Trade-offs

- [Risk] DPP 再現性テストが乱択実装差で不安定になる
  -> Mitigation: batch 全順序ではなく index 集合/一致の不変条件で評価する。

- [Risk] リネームで参照が壊れる
  -> Mitigation: OpenSpec と実行コマンド記載を同時に更新し、`pytest --collect-only` で検証する。
