## 1. Spec update

- [x] 1.1 Create OpenSpec proposal/design/spec artifacts for DPP sampler initialization timing
- [x] 1.2 Verify artifact completion status

## 2. Implementation

- [x] 2.1 Add initialization-state check API to DPPBatchSampler
- [x] 2.2 Refactor contrastive sampler refresh logic and call it at on_fit_start and on_train_epoch_start
- [x] 2.3 Re-run minimal DPP training command and confirm uninitialized RuntimeError is resolved
