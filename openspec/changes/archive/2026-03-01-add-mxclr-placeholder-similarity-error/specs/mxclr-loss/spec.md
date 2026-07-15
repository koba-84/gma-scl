## ADDED Requirements

### Requirement: MXCLR placeholder similarity must fail explicitly

`src/models/loss/mxclr.py` の類似度グラフ生成は、正式な類似度実装が導入されるまで暫定実装を使用してはならない。`MXCLR.similarity_graph` は MUST `NotImplementedError` を送出しなければならない。

#### Scenario: Calling similarity graph helper

- **WHEN** 開発者が `MXCLR.similarity_graph(labels)` を呼び出す
- **THEN** `NotImplementedError` が送出される

### Requirement: MXCLR self-test must validate placeholder behavior

`src/models/loss/mxclr.py` の自己テストは、未実装プレースホルダ挙動を MUST 検証し、エラー未発生を失敗として扱わなければならない。

#### Scenario: Run mxclr self-test

- **WHEN** 開発者が `uv run python src/models/loss/mxclr.py` を実行する
- **THEN** `NotImplementedError` の発生検証を含む自己テストが成功し、終了コード 0 で完了する
