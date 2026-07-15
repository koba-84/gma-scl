## Why

MXCLR は現時点で最終仕様が固まっておらず、AAPD で利用可能なラベル説明情報を類似度グラフへ反映できていない。ラベル説明文を Sentence-BERT で埋め込み、ラベル間の意味類似度を初期化時に確定できるようにして、暫定的なラベル共起依存のみの挙動から前進させる。

## What Changes

- `src/models/loss/mxclr.py` の `MXCLR.__init__` に、AAPD のラベル説明ファイルを使ってラベル間類似度行列を初期化する処理を追加する。
- 類似度は Sentence-BERT 埋め込みのコサイン類似度から計算し、loss 内で再利用できる形で保持する。
- AAPD 以外のデータセットや説明ファイル未指定時は、既存の labels 入力から生成する経路を維持する。
- `configs/contrastive/model/mxclr.yaml` に初期化用設定（dataset 名、説明ファイル、Sentence-BERT モデル名）を追加する。
- `src/models/loss/mxclr.py` の自己テストを、初期化契約変更を反映する形に更新する。
- **BREAKING**: `MXCLR.__init__` の入力契約が拡張され、設定不整合（AAPD 指定かつ説明ファイル不正）では初期化時に例外を送出する。

## Capabilities

### New Capabilities

- `mxclr-label-semantic-similarity`: AAPD ラベル説明文から Sentence-BERT ベースのラベル間類似度行列を生成し、MXCLR 初期化時に利用可能にする。

### Modified Capabilities

- `training`: MXCLR の初期化契約に、ラベル説明由来の意味類似度行列構築オプションを追加する。

## Impact

- 影響コード: `src/models/loss/mxclr.py`, `configs/contrastive/model/mxclr.yaml`, `tests/configs.py`, `tests/train.py`
- 依存: `sentence-transformers`（Sentence-BERT 利用）
- 影響運用: AAPD で semantic 類似度を使う場合は説明ファイルとモデル名の設定が必須になる
