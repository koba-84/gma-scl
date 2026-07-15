## Context

外部参照元の MulSupCon 実装は、batch 内の各サンプルについて positive になっている各ラベルを 1 行ずつ展開し、そのラベルを持つサンプル集合を positives とする supervised contrastive loss を計算している。一方、現行 `src/models/loss/ml_supcon.py` は label overlap の Jaccard 類似度を pairwise weight として使っており、`src/models/loss/base.py` と同型である。

## Goals / Non-Goals

**Goals**
- `MulSupCon` を label-wise expanded supervised contrastive として復元する。
- 埋め込み正規化は既存契約どおり `ContrastiveLitModule` 側に委ね、loss 実装で重複しない。
- pytest で `MulSupCon` の有限スカラー返却と `Base` との差分を検証する。

**Non-Goals**
- 外部実装の class 名や未使用引数をそのまま持ち込むこと
- `Base` loss の仕様変更
- queue ベース実装や multi-view 拡張

## Decisions

### 1. 各正ラベルを 1 行の contrastive row へ展開する

- Why: MulSupCon 固有の意味は「サンプル単位」ではなく「サンプル中の各正ラベル単位」で positives を定義する点にあるため。
- Chosen: `torch.where(labels_bin > 0)` で `(sample_idx, label_idx)` を抽出し、各 `(i, c)` を 1 行として similarity 行列と positive mask を構築する。
- Alternatives:
  - Jaccard 重み付きの sample-wise objective を流用する: `Base` と区別できず不適切。
  - ラベルごとに batch をループして loss を平均する: Python loop が増え、現行コードの vectorized 方針から外れる。

### 2. 自己ペアだけを除外し、同一ラベルを持つ他サンプルを positives とする

- Why: 元実装の意図は、同一サンプルの自己比較を除きつつ、同じラベルを持つ全サンプルを positives とする supervised contrastive だから。
- Chosen: 展開後 row ごとに anchor sample index と一致する列だけを除外し、`ref_labels[:, label_idx]` が 1 の列を positives とする。
- Alternatives:
  - 同一ラベル以外の overlap も positives に含める: MulSupCon ではなく別 objective になる。

### 3. 展開 row は等重みで平均する

- Why: 外部参照元の MulSupCon は展開後の各 row を一様重みで集約しており、まずはその objective を忠実に復元する必要があるため。
- Chosen: 展開された label-wise rows の loss を単純平均する。
- Alternatives:
  - サンプルごとの逆ラベル数で再重み付けする: 元実装と異なる objective になる。

## Risks / Trade-offs

- 正ラベルを持たないサンプルは展開対象外になる。これは MulSupCon の定義に沿うが、zero-label sample を含む batch では `Base` と振る舞いが異なる。
- 展開後 row 数は `sum_i |Y_i|` になるため、ラベル密度が高い batch では `Base` より計算量が増える。

## Validation Plan

1. `tests/losses/test_ml_supcon_loss.py` で有限スカラー返却、shape guard、`Base` と異なる loss 値を確認する。
2. `uv run pytest tests/losses/test_ml_supcon_loss.py tests/losses/test_base_loss.py`
3. `uv run pre-commit run --files src/models/loss/ml_supcon.py tests/losses/test_ml_supcon_loss.py openspec/changes/restore-mulsupcon-loss/proposal.md openspec/changes/restore-mulsupcon-loss/design.md openspec/changes/restore-mulsupcon-loss/tasks.md openspec/changes/restore-mulsupcon-loss/specs/training/spec.md openspec/specs/training/spec.md`
