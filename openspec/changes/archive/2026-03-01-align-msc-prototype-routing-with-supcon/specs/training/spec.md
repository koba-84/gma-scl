## MODIFIED Requirements

### Requirement: MSC must use externally provided prototypes in standard training path

MSC は標準学習経路で `loss_fn(z, labels, prototype)` を MUST 受け取り、`prototype` 未指定時に内部自動生成してはならない。`contrastive/model=msc` のとき、学習ステップは学習可能 prototype を正規化して MSC へ明示供給しなければならない。

#### Scenario: Route normalized learnable prototype to MSC loss

- **WHEN** 開発者が `contrastive/model=msc` で contrastive 学習を実行する
- **THEN** `ContrastiveLitModule` はラベル数×射影次元の学習可能 prototype を保持する
- **AND** 学習ステップで正規化した prototype を `MSC.forward(..., prototype=...)` に渡す

#### Scenario: Fail fast when prototype is missing for MSC

- **WHEN** `MSC.forward` が `prototype` 未指定で呼び出される
- **THEN** MSC は明示的な例外を送出し、暗黙の内部生成へフォールバックしない
