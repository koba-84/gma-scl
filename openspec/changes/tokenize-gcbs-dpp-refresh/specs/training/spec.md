## ADDED Requirements

### Requirement: Tokenized sampler refresh path for GCBS and DPP
When contrastive sampler refresh recomputes embeddings for GCBS or DPP, the system MUST use tokenized tensor batches and MUST NOT require raw text reconstruction inside the refresh loop.

#### Scenario: GCBS refresh uses tokenized tensors
- **WHEN** sampler_type is `gcbs` and epoch refresh runs
- **THEN** embeddings are recomputed from `input_ids` and `attention_mask` batches
- **AND** no raw text tokenization call is required during refresh

#### Scenario: DPP refresh uses tokenized tensors
- **WHEN** sampler_type is `dpp` and epoch refresh runs
- **THEN** embeddings are recomputed from `input_ids` and `attention_mask` batches
- **AND** resulting embeddings are passed to DPP sampler initialization
