## ADDED Requirements

### Requirement: Train tests must use hermetic synthetic datasets
Repository train tests MUST construct their own CSV dataset fixtures and MUST NOT depend on checked-out research datasets under `data/`.

#### Scenario: Run train tests in CI without repository datasets
- **WHEN** `tests/train.py` executes on a clean CI runner
- **THEN** the test fixture creates train/dev/test CSV files under a temporary directory
- **AND** `train(cfg_train)` completes without requiring `data/aapd/train.csv`
