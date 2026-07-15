## Context

現状の MCACR 実装は NPMI 行列を外部 `.npy` ファイルへ依存していた。今回の方針では依存ファイルを廃止し、loss 初期化ごとに `train.csv` から直接 NPMI を再計算する。

## Goals / Non-Goals

**Goals:**

- `data_dir` と `dataset_name` を入力として、MCACR 初期化時に毎回 NPMI を計算して学習を開始できる。
- 既存 `scripts/build_npmi.py` と同じ計算ロジックで値の意味を揃える。
- 失敗時の例外原因（CSV 欠如、形式不正）を明確化する。

**Non-Goals:**

- NPMI 計算式の変更。
- 他 loss への計算ロジック展開。
- 学習中に毎 step 再計算する動的更新。

## Decisions

1. `MCACRLoss` の初期化引数を `npmi_path` から `data_dir` と `dataset_name` へ変更し、`_load_npmi` で毎回 CSV から計算する。
   理由: `.npy` の有無に依存しない明示的な API にできる。
   代替案: `npmi_path` を残して暗黙に `train.csv` を探索。却下理由: 依存関係が不明瞭になる。

2. Hydra 設定も `data_dir: ${contrastive.data.data_dir}` と `dataset_name: ${contrastive.data.dataset_name}` に統一する。
   理由: データ設定と同じ情報源から一意に解決でき、loss 設定内のパス重複をなくせる。
   代替案: 既定推論（dataset 名から内部生成）。却下理由: 明示性が下がる。

3. 計算ロジックは `scripts/build_npmi.py` と同等実装を `mcacr.py` 内に持つ。
   理由: スクリプトを import せずにライブラリ実行時の依存を安定化できる。
   代替案: スクリプト関数を import。却下理由: 実行パス依存と循環参照リスクがある。

## Risks / Trade-offs

- [Risk] 毎回 NPMI 再計算するため初期化時間が増える。
  Mitigation: 方針として前処理削減を優先し、必要なら将来 change でキャッシュ機構を別途追加する。
- [Risk] `train.csv` 形式が想定外の場合に失敗する。
  Mitigation: 行番号・列番号を含む ValueError で即時に原因を示す。
- [Risk] 大規模データセットでは再計算コストが高い。
  Mitigation: 運用で必要な場合はバッチサイズや実験本数を考慮し、将来要件として計算結果キャッシュを検討する。
