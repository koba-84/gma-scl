## MODIFIED Requirements

### Requirement: Contrastive DataLoader sampler compatibility

The contrastive training dataloader MUST construct DataLoader arguments that satisfy PyTorch mutual exclusivity rules for samplers.

#### Scenario: DPP sampler uses batch_sampler-only mode

- **WHEN** `sampler_type` is `dpp` and `train_batch_sampler` is initialized
- **THEN** the dataloader SHALL be created with `batch_sampler`
- **THEN** the dataloader SHALL NOT pass `batch_size`, `shuffle`, `sampler`, or `drop_last`

#### Scenario: GCBS sampler keeps sample-order mode

- **WHEN** `sampler_type` is `gcbs` and `train_sampler` is initialized
- **THEN** the dataloader SHALL pass `sampler` with `batch_size`
- **THEN** the dataloader SHALL NOT pass `batch_sampler`
- **THEN** `shuffle` SHALL be `False`

#### Scenario: Default shuffle mode keeps batch_size path

- **WHEN** `sampler_type` is neither `dpp` nor `gcbs`
- **THEN** the dataloader SHALL pass `batch_size` and `shuffle=True`
- **THEN** the dataloader SHALL NOT pass `sampler` or `batch_sampler`
