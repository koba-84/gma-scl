## 1. Contrastive z normalization ownership

- [x] 1.1 Move `z` row-wise L2 normalization into each contrastive loss (`Base`, `MulSupCon`, `MCACRLoss`, `MCACRWONEG`, `MXCLR`, `MXCLRKendall`, `MSC`), remove caller-side normalization dependency from `ContrastiveLitModule`, and update loss tests to match the new contract.
