## Context

前段の修正で参照ファイル名自体は正したが、`label_description_path` は still relative path のままだった。CI の test では cwd が必ずしも repo root と一致しないため、`data/aapd/label_descriptions.json` は存在しても `Path(path)` が失敗する。

## Goals / Non-Goals

**Goals:**

- MXCLR の既定 path を cwd 非依存にする
- 既存の `PROJECT_ROOT` / `paths.root_dir` 契約と整合させる

**Non-Goals:**

- MXCLR 実装本体の path fallback 追加
- ラベル説明 JSON の保存場所変更

## Decisions

- Decision 1: config 値を `${paths.root_dir}/data/aapd/label_descriptions.json` に変更する
  - Rationale: 既存のパス契約に乗るだけで CI とローカルの両方を揃えられる
  - Alternative considered: 実装側で相対パスを `PROJECT_ROOT` 基準に補正する
  - Rejected because: config で表現できる責務をコードへ持ち込む必要がない

## Risks / Trade-offs

- [Risk] `PROJECT_ROOT` 契約を外した呼び出しでは引き続き失敗する → Mitigation: この repo は既に `paths.root_dir=${oc.env:PROJECT_ROOT}` 契約を採用しており、既存仕様と一致する
