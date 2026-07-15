## MODIFIED Requirements

### Requirement: DPP sampler numerical stability

When contrastive sampler type is DPP, the system SHALL use numerically stable settings for exact k-DPP sampling to avoid probability normalization failures on production-scale datasets.

#### Scenario: DPP embeddings are represented in float64

- **WHEN** DPP embeddings are set for batch sampling
- **THEN** the internal matrix representation SHALL use float64 precision

#### Scenario: Default DPP mode is GS_bis

- **WHEN** DPP mode is not explicitly specified in config
- **THEN** the sampler mode SHALL default to `GS_bis`

#### Scenario: aapd one-epoch run succeeds without probability-sum failure

- **WHEN** training is executed on aapd with `sampler_type=dpp`
- **THEN** the run SHALL not fail with `ValueError: probabilities do not sum to 1`

#### Scenario: DPP sampler does not emit third-party initialization prints

- **WHEN** DPP sampler constructs `FiniteDPP` with `L_gram_factor`
- **THEN** third-party informational prints SHALL NOT be emitted to standard output
