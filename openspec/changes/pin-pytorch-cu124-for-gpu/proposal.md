## Why

Python 3.12 移行後の uv lock は PyPI 既定の `torch 2.11.0+cu130` と `torchvision 0.26.0+cu130` を解決したが、ローカル GPU マシンの NVIDIA driver 555.42.06 は CUDA 12.5 世代までの互換であり、CUDA 初期化が失敗している。研究実装として GPU 検証を再現可能に戻すには、PyTorch 系だけをドライバ互換な公式 wheel index へ固定し、Python 3.12 baseline と両立させる必要がある。

## What Changes

- uv の package index 設定を追加し、`torch` と `torchvision` を PyTorch 公式の CUDA 12.4 wheel index から解決する。
- PyTorch 系の source pin を lockfile に反映し、Python 3.12 環境を再同期する。
- GPU 実行確認を `torch.cuda` smoke と最小 CUDA tensor 実行で再検証する。
- README / OpenSpec に、PyTorch 系が PyPI 既定ではなく GPU 互換 index から解決される理由を記録する。

## Capabilities

### New Capabilities

### Modified Capabilities
- `python-runtime-baseline`: Python 3.12 baseline で GPU を使う際の PyTorch wheel source と driver 互換要件を明示する。

## Impact

- 影響範囲: `pyproject.toml`, `uv.lock`, `README.md`, `openspec/project.md`, `openspec/specs/python-runtime-baseline/spec.md`
- 依存影響: `torch` / `torchvision` の取得元を PyTorch 公式 CUDA 12.4 index に固定
- 検証影響: `torch.cuda.is_available()`、CUDA tensor 生成、Ruff / mypy / pre-commit、必要最小限の pytest / smoke 再確認
