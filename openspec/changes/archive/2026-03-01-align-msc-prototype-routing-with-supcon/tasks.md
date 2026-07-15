## 1. OpenSpec/Config 更新

- [x] 1.1 `training` capability の delta spec を追加して MSC の prototype 契約変更を明記する
- [x] 1.2 `configs/contrastive/model/msc.yaml` に学習可能 prototype 経路を有効化する設定を追加する

## 2. 実装

- [x] 2.1 `ContrastiveLitModule` に学習可能 prototype の初期化・正規化・MSC への明示供給を実装する
- [x] 2.2 `src/models/loss/msc.py` の prototype 自動生成分岐を削除し、未指定時に例外を送出する

## 3. 検証

- [x] 3.1 `uv run python src/models/loss/msc.py` が成功するよう自己テストを更新する
- [x] 3.2 `uv run pytest tests/configs.py -q` で設定解決・instantiate が通ることを確認する
- [x] 3.3 `openspec/specs/training/spec.md` へ最終仕様を反映する
