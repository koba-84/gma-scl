## MODIFIED Requirements

### Requirement: Training internals must use canonical inline normalization

Training-related modules MUST implement row-wise L2 normalization by calling `torch.nn.functional.normalize` directly. For contrastive loss execution, normalization ownership MUST live in each contrastive loss implementation, and the training module MUST NOT require caller-side pre-normalization of `z`.

#### Scenario: Normalize contrastive embeddings and prototypes inline

- **WHEN** 開発者または coding agent が contrastive module や contrastive loss 実装を更新する
- **THEN** 行方向 L2 正規化は torch.nn.functional.normalize を直接呼び出して実装される
- **AND** normalize_embeddings や _normalize_prototype のような単純 wrapper は残さない
- **AND** `Base` `MulSupCon` `MCACRLoss` `MCACRWONEG` `MXCLR` `MXCLRKendall` `MSC` は loss 計算時に `z` を内部で正規化する
- **AND** `ContrastiveLitModule` は loss 呼び出しに必要な `z` 正規化を事前条件として持たない
