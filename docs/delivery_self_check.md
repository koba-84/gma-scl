# Delivery Self Check

報告漏れを防ぐため、最終報告の直前に以下を実行する。

## 1. 実行コマンド

```bash
bash scripts/verify_delivery.sh \
  --changes add-classification-asl-zlpr-loss,refactor-classification-config-axis \
  --run "uv run pytest tests/test_configs.py -q" \
  --run "uv run python src/train.py --cfg job --resolve 'classification/strategy@classification.model=linear_probe' 'classification/loss@classification.model=asymmetric' > /dev/null" \
  --run "uv run python src/train.py --cfg job --resolve 'classification/strategy@classification.model=finetune' 'classification/loss@classification.model=zlpr' > /dev/null"
```

## 2. チェック項目

- 直近 commit 一覧が出力される
- 指定した OpenSpec change がすべて complete である
- 指定した検証コマンドがすべて成功する
- ワークツリー状態が表示される

## 3. 報告テンプレート

スクリプトが出力する Report Template をそのまま埋めて報告する。
最低限、以下を必ず記載する。

- 変更概要
- commit 粒度（commit ごとの目的）
- 実行検証（実コマンドと結果）
- OpenSpec change と状態
- 未実施項目または既知リスク
