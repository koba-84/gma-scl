## ADDED Requirements

### Requirement: MCACR_WONEG loss class

The system MUST provide a contrastive loss class named `MCACR_WONEG` that computes MCACR attraction with the existing formulation and computes repulsion without label-based negative weights.

#### Scenario: Instantiate MCACR_WONEG from target path

- **WHEN** a developer instantiates `src.models.loss.mcacr_woneg.MCACR_WONEG` with a valid `.npy` NPMI path
- **THEN** the object SHALL initialize successfully
- **AND** it SHALL validate NPMI shape and label dimension in the same way as `MCACRLoss`

#### Scenario: Repulsion uses distance-only weighting

- **WHEN** `MCACR_WONEG.forward` is called with valid embeddings and labels
- **THEN** the attraction term SHALL use the same label-overlap weighting as `MCACRLoss`
- **AND** the repulsion term SHALL be computed without label-derived negative weights
