## MODIFIED Requirements

### Requirement: Tokenized dataset access must reuse tensor-backed rows

Tokenized dataset access MUST avoid rebuilding tensors for model-facing columns on every `__getitem__` call once the cached split has been prepared.

#### Scenario: Reuse tensor-backed tokenized columns during item access

- **WHEN** 開発者または coding agent が tokenized cache を読み込んだ split から sample を取得する
- **THEN** `input_ids`, `attention_mask`, `labels`, `is_empty_text` は tensor-backed row として取得される
- **AND** `__getitem__` は Python list から新しい tensor を都度構築しない
- **AND** 返却される dtype は `input_ids` / `attention_mask` が `torch.long`, `labels` が `torch.float32`, `empty_text_mask` が `torch.bool` を維持する
