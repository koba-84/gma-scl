## Context

現行実装では `Encoder.forward` が文字列バッチを受け、毎ステップ `AutoTokenizer` を実行する。DataModule は CSV 由来の text/label をそのまま返すため、CPU 前処理が反復実行される。今回の変更は DataModule・Encoder・LightningModule の入力契約を横断的に変更するため、設計を先に固定する。

## Goals / Non-Goals

**Goals:**
- Hugging Face Datasets による train/dev/test の事前トークナイズを標準化する。
- tokenized cache を再利用し、同一設定で再現可能な前処理経路を提供する。
- classification/contrastive の両ステージで tokenized batch 契約を統一する。

**Non-Goals:**
- モデル構造・loss 関数の変更
- GCBS/DPP アルゴリズム自体の変更
- 推論専用パイプラインの最適化

## Decisions

- Decision 1: 前処理ヘルパーを `src/data/components/hf_tokenized_dataset.py` に新設する。
  Rationale: DataModule から tokenizer/caching ロジックを分離し、classification と contrastive で共通利用する。

- Decision 2: DataModule が返すバッチ契約を dict ベース（`input_ids`, `attention_mask`, `labels`）へ統一する。
  Rationale: モデル内トークナイズを廃止し、学習ステップ中の CPU 負荷を削減する。

- Decision 3: `Encoder.forward` を tokenized tensors 入力のみに最適化する。
  Rationale: 旧 text list 経路を残すと分岐と保守コストが増えるため、入力契約を一本化する。

- Decision 4: キャッシュキーに tokenizer 名・max_length・label列順を含める。
  Rationale: 設定変更時の誤キャッシュ再利用を防ぎ、再現性要件を満たす。

## Risks / Trade-offs

- [Risk] 初回 tokenization 時間が増える → Mitigation: 2回目以降は save_to_disk/load_from_disk を利用し再利用する。
- [Risk] 入力契約変更で既存テストが破壊される → Mitigation: 関連ユニットテストを同時更新し、契約を明示化する。
- [Risk] GCBS/DPP 経路で text 参照が必要な箇所が残る → Mitigation: sampler 更新に必要な raw text を dataset 内に保持し、埋め込み計算時にのみ参照する。

## Migration Plan

1. 依存に `datasets` を追加し、共通前処理ヘルパーを実装する。
2. classification DataModule と Finetune モジュールを tokenized batch 契約へ移行する。
3. contrastive DataModule と Contrastive モジュールを同契約へ移行し、GCBS/DPP 更新経路を調整する。
4. 設定ファイルを更新し、tokenizer/max_length/cache パラメータを DataModule 側へ寄せる。
5. 関連テストを更新して新契約を固定する。

## Open Questions

- DPP/GCBS の埋め込み更新頻度と cache invalidate ポリシーをどこまで設定化するか。
- 将来の複数 tokenizer 比較実験で cache ディレクトリをどう階層化するか。
