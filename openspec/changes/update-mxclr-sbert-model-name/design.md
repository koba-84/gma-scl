## Design

MXCLR のラベル説明文エンコーダは Hydra 設定と Python 実装の両方に既定値を持つ。再現性を崩さないため、両者を同じモデル名に保つ。

### 変更方針

- Hydra 既定値 `configs/contrastive/model/mxclr.yaml` の `contrastive.model.loss_fn.sbert_model_name` を更新する
- Python 側既定値 `src/models/loss/mxclr.py` の `MXCLR.__init__` を同じ文字列へ更新する
- config compose の回帰テストで解決値を固定する

### 非対象

- rank/proto 系の未マージブランチ固有実装
- `sbert_max_length` や他の MXCLR ハイパーパラメータ
