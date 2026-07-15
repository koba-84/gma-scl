## Context

`src/train.py` の `_run_stage()` は `stage_cfg.get("callbacks", base_cfg.get("callbacks"))` を `instantiate_callbacks()` に渡す。contrastive stage は `configs/contrastive/train.yaml` で `callbacks: null` を持つため debug config と整合するが、classification stage は `configs/classification/train.yaml` で `${callbacks.model_checkpoint}` などを参照する stage-local callbacks を定義している。このため global `callbacks: null` だけでは debug 時に classification の補間が壊れる。

## Goals / Non-Goals

**Goals**
- debug config が callbacks 無効化を contrastive / classification 両 stage に一貫適用できるようにする。
- 通常学習時の callbacks 構成は変更しない。
- Python 3.12 + GPU 環境で fast_dev_run を完走させる。

**Non-Goals**
- callback instantiation ロジックの一般化
- 通常学習用 callback 設定の再設計
- trainer / model 実装の変更

## Decisions

### 1. debug/default.yaml で classification.callbacks を明示的に null override する

- Why: 既存の stage-local callback 参照を通常学習では維持しつつ、debug 時だけ補間元欠落を防ぐ最小変更だから。
- Chosen: `configs/debug/default.yaml` に `classification.callbacks: null` を追加する。
- Alternatives:
  - `configs/classification/train.yaml` から stage-local callbacks を削除する: 通常学習時の checkpoint 運用まで変わるため過剰。
  - `instantiate_callbacks()` 側で補間失敗を握りつぶす: 設定破損の検知を弱めるため不適切。

## Risks / Trade-offs

- debug/default では classification test 時に checkpoint callback がなくなるが、`src/train.py` は checkpoint 未作成時に current weights で test するため fast_dev_run では許容できる。
- debug 時の progress bar / model summary も無効になるが、debug config の「callbacks を無効化する」という既存意図と一致する。

## Validation Plan

1. `uv run python src/train.py --config-name test --cfg job --resolve debug=fdr ...` で `classification.callbacks` が `null` と解決されることを確認する。
2. `uv run python src/train.py --config-name test debug=fdr ...` を Python 3.12 + GPU 環境で実行し、contrastive / classification の fast_dev_run 完走を確認する。
3. 関連ファイルに対して `uv run pre-commit run --files ...` を実行する。
