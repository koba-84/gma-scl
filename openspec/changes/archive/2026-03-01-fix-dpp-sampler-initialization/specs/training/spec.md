## MODIFIED Requirements

### Requirement: Contrastive dynamic sampler initialization timing

The contrastive training pipeline MUST initialize dynamic samplers before the first train dataloader iteration when the sampler requires runtime embeddings.

#### Scenario: DPP sampler is initialized before first training iterator

- **WHEN** `sampler_type` is `dpp` and `trainer.fit` starts
- **THEN** the system SHALL compute embeddings and call `set_embeddings` before first train dataloader iteration
- **THEN** `DPPBatchSampler` SHALL NOT raise an uninitialized error at the start of epoch 0

#### Scenario: DPP sampler is refreshed per epoch

- **WHEN** each training epoch starts with `sampler_type=dpp`
- **THEN** the system SHALL refresh embeddings for DPP batch sampling

#### Scenario: Non-DPP samplers retain existing behavior

- **WHEN** `sampler_type` is `gcbs` or default shuffle
- **THEN** existing sampler update behavior SHALL remain unchanged
