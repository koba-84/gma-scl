## Context

`src/train.py` は学習開始時に `if cfg.get("seed"):` で分岐しており、Hydra 設定で `seed: 0` の場合は偽判定となって `lightning.seed_everything` が呼ばれない。結果として、seed を 0 に固定した実験が非決定になり、再現性要件と矛盾する。

## Goals / Non-Goals

**Goals:**
- seed が数値で指定された場合（0 を含む）に必ずシード初期化を実行する。
- seed が未設定（None）の場合のみシード初期化を省略する。
- 挙動を仕様へ明文化する。

**Non-Goals:**
- deterministic 設定や CUDA の非決定性制御の変更。
- DataLoader の shuffle 挙動や sampler 戦略の変更。

## Decisions

- seed 初期化条件を「truthy 判定」から「None でない判定」へ変更する。
  - 採用案: `if cfg.get("seed") is not None:`
  - 不採用案: `if cfg.seed >= 0`（負値 seed を不必要に禁止するため不採用）
- 変更箇所は `src/train.py` のみとし、影響を最小化する。
- training spec に seed 指定時の必須挙動（seed=0 含む）を ADDED requirement として追記する。

## Risks / Trade-offs

- [Risk] seed 未設定時に既存実験との差分が不明瞭になる可能性
  → Mitigation: None 判定を明示し、未設定時は従来通り非固定であることを仕様に記載する。
- [Trade-off] seed=0 実験の結果が従来 run と一致しなくなる
  → Mitigation: これまでが仕様不一致であり、再現性要件優先で修正する。
