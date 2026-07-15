- [x] 1. Update default runtime configs for pin_memory and compile
  - Set `pin_memory: True` in contrastive/classification tokenized data configs.
  - Set `compile: true` in default contrastive/classification model configs.
  - Validate with config resolve command.

- [x] 2. Remove per-sample tensor reconstruction in tokenized dataset access
  - Keep tokenized Hugging Face splits in torch format for model-facing columns.
  - Update `TokenizedTorchDataset.__getitem__` to reuse tensor-backed rows without rebuilding tensors every access.
  - Validate with targeted pytest for tokenized dataset behavior.
