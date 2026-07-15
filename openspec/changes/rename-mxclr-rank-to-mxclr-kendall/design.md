## Context

現状の ranking loss 実体は Kendall τ だが、Hydra model 名や Python クラス名が `rank` のまま残っている。研究コードでは設定名がそのまま実験ラベルや比較軸になるため、命名不一致は再現性レビュー時のノイズになる。

## Goals / Non-Goals

**Goals:**
- 公開識別子を `mxclr_kendall` / `MXCLRKendall` へ統一する。
- 実装ロジック（MXCLR + `lambda_rank * kendall_loss`）とハイパラ契約は変更しない。
- 旧名を参照する config/test/spec を一括更新する。

**Non-Goals:**
- Kendall loss 数式や重み付け戦略の変更
- 追加の loss バリアント導入
- 旧名互換レイヤーの提供

## Decisions

### Decision 1: モジュールファイルとクラス名を明示 rename する

- `src/models/loss/mxclr_rank.py` を `src/models/loss/mxclr_kendall.py` に rename し、`MXCLRRank` を `MXCLRKendall` に変更する。
- private helper も `_compute_mxclr_kendall_loss` に揃える。

### Decision 2: Hydra 公開エントリを `mxclr_kendall.yaml` に切り替える

- `configs/contrastive/model/mxclr_rank.yaml` を `mxclr_kendall.yaml` へ rename し、`_target_` 参照を更新する。
- 旧 `mxclr_rank` 設定は残さない。

### Decision 3: 参照面をテストと main spec まで同期する

- `tests/test_configs.py` と loss unit test を `mxclr_kendall` 名称へ更新する。
- `openspec/specs/training/spec.md` と `openspec/specs/training.md` の requirement 記述も同名へ更新する。

## Risks / Trade-offs

- [Risk] 旧 override (`contrastive/model=mxclr_rank`) を使う既存実験スクリプトが失敗する → Mitigation: breaking change を proposal/spec に明記し、以後 `mxclr_kendall` を唯一の公開名にする。
- [Risk] rename 漏れで import error が発生する → Mitigation: pytest + pre-commit で参照面を検証する。
