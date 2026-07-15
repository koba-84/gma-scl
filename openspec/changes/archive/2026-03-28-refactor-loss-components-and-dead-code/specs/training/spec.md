## MODIFIED Requirements

### Requirement: MXCLR transport helper contract must define shared inputs and outputs

The public helper in `src/models/loss/components/transport.py` MUST expose one canonical module contract: it accepts `labels_bin: [N, L]`, `cost_matrix: [L, L]`, `label_weights: [L]`, and an explicit transport strategy selector, and it returns a pairwise distance matrix `[N, N]`. Public helper names MUST NOT be split by transport family when the input/output contract is otherwise identical.

#### Scenario: Call shared transport helper for balanced families

- **WHEN** 開発者または coding agent が WMD または WRD の距離計算を呼び出す
- **THEN** 呼び出しは 1 つの公開 transport helper に strategy 指定で集約される
- **AND** WMD は active label frequency mass、WRD は active embedding-norm mass を使う

#### Scenario: Call shared transport helper for unbalanced family

- **WHEN** 開発者または coding agent が UOT の距離計算を呼び出す
- **THEN** 呼び出しは同じ公開 transport helper を使い strategy で unbalanced solver を選択する
- **AND** UOT は active embedding-norm mass を未正規化のまま使う

### Requirement: Label statistics and aggregation helpers must use concise canonical names

The public helpers in `src/models/loss/components/label_stats.py` and `src/models/loss/components/aggregation.py` MUST expose concise canonical names based on their documented module contracts. Label-set aggregation helpers and train.csv-derived label statistics MUST NOT remain duplicated in top-level loss modules.

#### Scenario: Compute label statistics from the shared train.csv contract

- **WHEN** 開発者または coding agent が label statistics helper を呼び出す
- **THEN** canonical helper 名は `compute_idf` と `compute_npmi` である
- **AND** `label_stats` module contract が label counts / pair counts / train.csv source を定義する
- **AND** MCACR は top-level loss module 内で train.csv 由来の統計計算を直接持たない

#### Scenario: Aggregate pairwise label-set similarity under the shared aggregation contract

- **WHEN** 開発者または coding agent が label-set aggregation helper を呼び出す
- **THEN** canonical helper 名は `aggregate_similarity` である
- **AND** helper は `labels_bin`, `similarity_matrix`, `agg`, optional `label_weights` を受け取り `[N, N]` の similarity matrix を返す
- **AND** top-level の `src/models/loss/aggregation.py` は存在しない
