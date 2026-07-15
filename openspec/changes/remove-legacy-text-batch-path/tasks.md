## 1. Artifacts

- [x] 1.1 Create proposal/design/spec/tasks for removing legacy text batch path
- [x] 1.2 Verify artifact status is apply-ready

## 2. Implementation

- [x] 2.1 Remove raw-text fallback branch from encoder and tighten model input typing
- [x] 2.2 Simplify classification/contrastive datamodule batch contract to `(inputs, labels)`
- [x] 2.3 Update finetune/contrastive modules and integration tests for no-text batch contract
