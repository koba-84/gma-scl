## Context

現在の runtime 依存は `transformers>=4.34.0` で上限がなく、uv は 2026-03-31 時点で `transformers 5.4.0` を解決している。リポジトリでは `sentence-transformers 5.3.0` を利用しており、実運用の encoder forward 経路で `transformers.utils.output_capturing` 配下の `NameError: name 'torch' is not defined` が発生しているため、問題は学習コードではなく Hugging Face runtime の major 更新にある。

## Goals / Non-Goals

**Goals:**
- `transformers` の解決結果を安定な 4 系へ戻し、既存 encoder 実装で forward が通る状態を再現可能にする。
- `sentence-transformers` の要求範囲と矛盾しない制約を `pyproject.toml` と `uv.lock` に残す。
- 将来の `uv lock --upgrade` でも無条件に 5 系へ上がらないよう、spec に major 系列制約の根拠を記録する。

**Non-Goals:**
- Hugging Face 5 系への追従実装
- encoder / model forward ロジック自体の変更
- `sentence-transformers` の差し替えや大規模な依存更新

## Decisions

### 1. `transformers` に `<5` の上限を追加する

- Why: 今回の障害は 5.4.0 で発生し、現行コードと依存構成で 4 系の単純 import / forward は通っているため。
- Chosen: `pyproject.toml` を `transformers>=4.41.0,<5` に更新し、`sentence-transformers 5.3.0` の要求下限とも揃える。
- Alternatives:
  - exact pin: 再現性は高いが、このリポジトリの「下限 + lockfile」運用から外れる。
  - 5 系に合わせてコード修正: 原因が外部依存の不安定化であり、研究コード側に暫定互換対応を持ち込むべきではない。

### 2. 検証は import と最小 forward smoke に絞る

- Why: 問題の本質は dependency resolution と runtime import/forward の整合性であり、全学習ジョブを回す前に最小再現で切り分けるほうが適切なため。
- Chosen: `transformers` version 確認、`AutoModel.from_config` による最小 forward、既存 `Encoder` の forward smoke を実行する。
- Alternatives:
  - いきなりフル学習実行: GPU 時間を消費し、依存障害の切り分けが不明瞭になる。

## Risks / Trade-offs

- [transformers 5 系でしか使えない新機能は入らない] → 本リポジトリでは 5 系依存機能を使っておらず、安定性を優先する。
- [4 系内で将来別の回帰が入る] → `<5` に加えて `uv.lock` を更新し、解決結果を固定する。
- [補助マニフェストの記述が残る] → 正本は `pyproject.toml` と `uv.lock` なので、まずそこを是正し、必要なら後続 change で legacy マニフェストを整理する。
