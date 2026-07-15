## ADDED Requirements

### Requirement: MCACR の NPMI 直接計算

`src.models.loss.mcacr.MCACRLoss` は、MUST `data_dir` と `dataset_name` を入力として受け取り、`<data_dir>/<dataset_name>/train.csv` から直接 NPMI 行列を計算しなければならない。

#### Scenario: NPMI ファイルなしで初期化できる

- **WHEN** 開発者が `data_dir` と `dataset_name` を指定して `MCACRLoss` を初期化する
- **THEN** 実装は NPMI ファイルを読み書きせずに NPMI 行列を計算し、初期化が成功する

#### Scenario: 必要入力が無い場合は明示的に失敗する

- **WHEN** 解決された `<data_dir>/<dataset_name>/train.csv` が存在しない
- **THEN** 初期化は MUST `FileNotFoundError` を送出し、欠落した入力パスをエラーメッセージに含める
