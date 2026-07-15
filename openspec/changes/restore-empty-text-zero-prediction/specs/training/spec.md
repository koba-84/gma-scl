## ADDED Requirements

### Requirement: Empty-text prediction override on classification test
Classification test evaluation MUST set predictions to all-zero for rows identified as empty text by preprocessing metadata.

#### Scenario: Empty text row becomes zero prediction
- **WHEN** classification test_step processes a batch containing empty-text rows
- **THEN** prediction tensor rows for those samples are replaced with zero vector
- **AND** non-empty rows keep sigmoid-threshold predictions

#### Scenario: No raw text payload required
- **WHEN** empty-text override is applied
- **THEN** decision uses precomputed metadata flag from tokenized inputs
- **AND** runtime batch contract remains `(inputs, labels)`
