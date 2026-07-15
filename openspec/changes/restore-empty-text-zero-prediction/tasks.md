## 1. Artifacts

- [x] 1.1 Create proposal/design/spec/tasks for empty-text zero prediction restore
- [x] 1.2 Verify artifact status is apply-ready

## 2. Implementation

- [x] 2.1 Add empty-text metadata flag to tokenized preprocessing and datamodule collate
- [x] 2.2 Restore zero-prediction override in finetune test_step using metadata mask
- [x] 2.3 Update integration tests and run targeted pytest
