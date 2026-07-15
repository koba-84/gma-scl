## Context

ローカル GPU マシンの `nvidia-smi` 実測は Driver 555.42.06 / CUDA 12.5 だった。一方、Python 3.12 baseline 変更後の `uv lock --upgrade` は PyPI 既定から `torch 2.11.0+cu130` を解決し、`torch.cuda.is_available()` が driver too old で false になっている。CPU 側の Python 3.12 検証は通っているため、問題は Python runtime ではなく PyTorch wheel source の選択にある。

## Goals / Non-Goals

**Goals:**
- `torch` / `torchvision` だけを driver 互換な PyTorch 公式 CUDA 12.4 index へ固定する。
- Python 3.12 baseline と GPU 実行を両立し、lockfile に再現可能な形で残す。
- GPU smoke をローカルで実行し、CUDA tensor 生成まで確認する。

**Non-Goals:**
- NVIDIA driver の更新
- モデル / 学習ロジック / 設定の変更
- PyTorch 系以外の依存の大規模更新

## Decisions

### 1. PyTorch 系だけを explicit uv index へ pin する

- Why: 問題は PyPI 既定で解決される CUDA 13.0 wheel であり、全依存の index を変える必要はない。
- Chosen: `[[tool.uv.index]]` に PyTorch 公式 `cu124` index を追加し、`[tool.uv.sources]` で `torch` と `torchvision` のみをその index に固定する。
- Alternatives:
  - driver 更新: 環境変更が大きく、この change の責務を超える。
  - CPU wheel 固定: GPU 可用性の回復という目的を満たさない。
  - cu126 index: driver 12.5 との余裕が少なく、保守的でない。

### 2. 直接依存の下限は維持し、source pin で解決結果を制御する

- Why: 既存の Python 3.12 baseline 変更で `torch>=2.3.0`, `torchvision>=0.18.0` までは整理済みであり、今回は source pin が本質的変更点である。
- Chosen: version floor は据え置き、index/source と lock 更新に集中する。
- Alternatives:
  - exact version pin: 再現性は高いが、既存の「下限 + lockfile」運用から外れる。

## Risks / Trade-offs

- [PyTorch 公式 index 上の利用可能最新版が将来変わる] → 現時点の exact resolution は `uv.lock` に固定し、source pin も残す。
- [他 OS で CUDA wheel が不要] → source pin は PyTorch 公式 index 由来でも wheel 解決可能だが、README に GPU 互換意図を明記する。
- [pytest の既存失敗が残る] → 今回は GPU driver 起因の失敗解消に集中し、データ未配置テストは既知の別要因として扱う。

## Migration Plan

1. OpenSpec で PyTorch source pin の要件を定義する。
2. `pyproject.toml` に uv index/source 設定を追加する。
3. `uv lock --upgrade` と `uv sync --all-groups` を実行する。
4. `torch.cuda` smoke、Ruff、mypy、pre-commit を再確認する。
5. main spec / project context を同期してコミットする。

## Open Questions

- なし。driver 実測値と PyTorch 公式 `cu124` wheel availability を根拠に保守的判断が可能。
