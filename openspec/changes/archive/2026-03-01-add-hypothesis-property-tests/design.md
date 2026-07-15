## Context

Ruff, mypy, pytest-cov は導入済みだが、入力空間の自動探索を行う property-based test は未導入である。特にサンプラやラベル演算の純関数は、ランダム化された入力に対する不変条件検証と相性が良い。

## Goals / Non-Goals

**Goals:**

- Hypothesis を dev 依存に導入する。
- 少なくとも2つの純関数に property-based test を追加する。
- ローカル品質コマンドとして実行手順を README に明示する。

**Non-Goals:**

- GPU 学習ループ全体を Hypothesis 対象にすること。
- 既存の integration テストを property-based test に置換すること。

## Decisions

1. 対象関数は純関数に限定する。

- 対象: `compute_gcbs_permutation` と `Base._compute_or`
- 理由: 外部依存や乱数状態の影響を受けにくく、安定して不変条件を表現できる。

2. 検証観点は「出力形状・順列性・可換性・値域」に限定する。

- 理由: 実装差分に強く、過度に内部実装へ依存しない。

3. 実行時間制御として Hypothesis profile は導入せず、初期はデフォルト設定を使う。

- 理由: 設定追加を最小化し、まず導入を完了させる。

## Risks / Trade-offs

- [Risk] 入力空間が広いとテスト時間が増える。
  Mitigation: 対象関数を小さく保ち、strategy 上限を設定する。
- [Risk] 浮動小数点境界で不安定な失敗が起きる。
  Mitigation: finite 値に限定し、許容誤差を利用する。

## Validation Plan

- `uv run pytest tests/property_based.py`
- `uv run pre-commit run -a`
