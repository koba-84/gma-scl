## MODIFIED Requirements

### Requirement: Pytest train/eval suite boundaries must remain explicit

Training-related pytest modules MUST align file boundaries with marker boundaries so fast, slow, integration, and GPU suites can be understood from module layout.

#### Scenario: Add or update a CPU integration-only training module

- **WHEN** 開発者または coding agent が CPU で実行する train/eval/data integration pytest module を追加または更新する
- **THEN** module-level marker はその suite 所属と一致する
- **AND** `slow` または `gpu` を含む case は別 module へ分離される

#### Scenario: Run targeted pytest modules from documentation

- **WHEN** 開発者が README または spec の実行例に従って targeted pytest を実行する
- **THEN** 実行例は標準 discovery 命名に従う実在ファイルを指す
- **AND** train 系の targeted 実行例は CPU integration、CPU slow、GPU、GPU slow を分けて参照できる
