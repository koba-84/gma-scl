## Context

外部の大規模 ML OSS（Transformers, PyTorch Lightning）では、重い統合テストとは別に高速な unit test を厚く持ち、CI の常時実行対象を軽量化している。また、ML テスト指針ではデータ契約の検証が失敗原因の早期検知に有効とされる。現リポジトリは train エントリポイント検証はあるが、データコンポーネントの境界条件テストが不足している。

## Goals / Non-Goals

**Goals:**

- サンプラー/データセット層で、GPU 非依存かつ秒オーダーで実行できる unit test を追加する。
- 入力バリデーションの異常系を明示的に検証し、失敗時メッセージの品質を担保する。
- training spec に unit/data-contract 層を追記し、運用ルールとして固定する。

**Non-Goals:**

- 学習アルゴリズム本体の変更。
- 既存 `tests/test_train.py`・`tests/test_sweeps.py` の置き換え。
- E2E の GPU 実行方針変更。

## Decisions

1. 対象を `gcbs`、`dpp`、`classification_dataset`、`classification_datamodule`、`contrastive_datamodule`、`mlp_head` に広げる。
   理由: 学習失敗の入口になりやすいデータ経路と軽量モデル部品を、統合テスト前に検証したいため。

2. unit test は対象実装ファイル末尾の `if __name__ == "__main__":` に配置する。
   理由: 実装とテストを近接させ、変更時の同時更新漏れを減らすため。

3. `classification_dataset` では CSV 異常入力（欠損列、非数値ラベル）を最低限カバーする。
   理由: ML で頻発するデータ品質起因の障害を学習実行前に遮断するため。

4. DataModule の自己テストでは、`multi-label/tmp` に最小 CSV を作成して `prepare_data` / `setup` / dataloader を通す。
   理由: 実データ依存を避けつつ、構成破損や sampler 初期化不備を早期検知できるため。

## Risks / Trade-offs

- [Risk] dppy の乱択で不安定化する可能性
  -> Mitigation: 厳密なサンプル順は検証せず、重複なし・全件被覆など不変条件を検証する。

- [Risk] 実装ファイルが長くなる
  -> Mitigation: 自己テストは境界条件の最小セットに限定し、重い検証は既存 pytest 統合テストに残す。
