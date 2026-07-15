## 1. Artifacts

- [x] 1.1 Create proposal/design/spec/tasks for HF Datasets tokenized pipeline
- [x] 1.2 Verify artifact status is apply-ready

## 2. Dependency and shared preprocessing

- [x] 2.1 Add `datasets` runtime dependency via uv and update lockfile
- [x] 2.2 Implement shared HF Datasets tokenization/cache helper in `src/data/components/hf_tokenized_dataset.py`

## 3. Training input contract migration

- [x] 3.1 Migrate classification datamodule and finetune module to tokenized batch contract
- [x] 3.2 Migrate contrastive datamodule and contrastive module to tokenized batch contract
- [x] 3.3 Update encoder forward path to consume tokenized tensors directly

## 4. Config and validation

- [x] 4.1 Update classification/contrastive data configs with tokenizer and cache parameters
- [x] 4.2 Update/add tests for new batch contract and run targeted pytest
