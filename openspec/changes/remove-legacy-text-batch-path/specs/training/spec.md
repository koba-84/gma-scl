## ADDED Requirements

### Requirement: Tokenized-only batch contract
Training modules MUST accept tokenized tensor batches only and MUST NOT keep raw-text fallback in mini-batch execution paths.

#### Scenario: Encoder rejects raw-text fallback path
- **WHEN** encoder forward is called from training modules
- **THEN** input contract requires tokenized tensors (`input_ids`, `attention_mask`)
- **AND** no internal text tokenization fallback branch exists in the training path

#### Scenario: Stage modules process `(inputs, labels)` batch tuple
- **WHEN** classification or contrastive training/validation/test step runs
- **THEN** batch format is `(tokenized_inputs, labels)`
- **AND** step logic does not branch on optional raw text payloads
