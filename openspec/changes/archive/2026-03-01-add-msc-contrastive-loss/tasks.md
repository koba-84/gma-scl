## 1. OpenSpec仕様反映

- [x] 1.1 training capability の命名・設定解決要件へ MSC を追加する
- [x] 1.2 loss 実装ファイル名の命名規則（src/models/loss/\<loss_name>.py、冗長接頭辞禁止）を仕様へ明記する

## 2. Loss実装

- [x] 2.1 src/models/loss/msc.py を追加して MSC を実装する
- [x] 2.2 MSC が loss_fn(z, labels) 契約で動作するよう prototype 内部生成経路を実装する
- [x] 2.3 src/models/loss/__init__.py に MSC を公開追加する

## 3. 設定と検証

- [x] 3.1 configs/contrastive/model/msc.yaml を追加し Hydra から解決可能にする
- [x] 3.2 uv run python src/models/loss/msc.py を実行して自己テストを確認する
- [x] 3.3 uv run pytest tests/configs.py -q を実行して設定解決を確認する
- [x] 3.4 ddp_sim 検証を修正（tests/train.py の ddp_sim テストを設定解決検証へ変更、stage trainer へ strategy 伝播追加）し、uv run pytest tests/train.py -q -k test_train_ddp_sim で 1 passed を確認する
- [x] 3.5 uv run pytest tests/eval.py -q を実行して通過を確認する
- [x] 3.6 uv run pytest tests/sweeps.py -q を実行し、Requires: [sh] により 3 件 skip を確認する
- [x] 3.7 scripts/test.sh は未実施（CUDA/precision/device 分岐変更なしのため本変更では対象外）と記録する
