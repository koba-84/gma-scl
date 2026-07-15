## Context

Transformers の testing ガイドでは、fast tests を PR で常時実行し、遅い学習系は slow として分離する運用を推奨している。PyTorch Lightning でも trainer 条件ごとの統合テストを重視しており、Data 経路の破損を早期検知することが重要である。TFDV の指針でも、学習前のデータ妥当性検証を重視している。

## Goals / Non-Goals

**Goals:**

- DataModule + sampler の統合経路を pytest で検証する。
- すべて CPU・tiny データで実行し、fast integration として `not slow` で回せるようにする。
- 正常系に加えて主要な失敗経路（未初期化 sampler、不整合 config）を検証する。

**Non-Goals:**

- GPU 学習統合テストの置き換え。
- モデル品質の最終評価（メトリクス閾値）追加。

## Decisions

1. テスト対象は DataModule 統合に限定する。
   理由: 現状のボトルネックが sampler/data 経路の回帰検知不足であり、最小変更で効果が大きいため。

2. テストデータは各テスト内で `multi-label/tmp` 配下に動的生成して破棄する。
   理由: 実データ依存を排し、環境差分を抑えるため。

3. `dpp` 経路は「埋め込み未設定では失敗」「設定後は batch 取得成功」の両方を必須とする。
   理由: 現実運用で起きやすい初期化順序ミスを直接検知するため。

## Risks / Trade-offs

- [Risk] テストが DataModule 自己テストと一部重複する
  -> Mitigation: pytest 側は「モジュール間接続」を主目的にし、詳細境界値は自己テスト側に委譲する。

- [Risk] テスト実行時間増
  -> Mitigation: tiny CSV と小 batch を使用し、1ファイルで高速に完了する粒度にする。
