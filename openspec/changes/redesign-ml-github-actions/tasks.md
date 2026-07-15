## 1. Artifacts

- [x] 1.1 Create proposal/design/spec/tasks for ML-oriented GitHub Actions redesign

## 2. Implementation

- [x] 2.1 Add ML CI shell entrypoints and pytest GPU marker contract, then validate local CPU CI reproduction
- [x] 2.2 Redesign GitHub Actions workflows around uv cache, concurrency, changed-file no-op, and artifacts, then validate YAML and local scripts
- [x] 2.3 Update README CI/testing guidance to match the new CPU/GPU verification split, then re-run required local checks
- [x] 2.4 Sync finalized CI requirements into main OpenSpec specs and verify change status
- [x] 2.5 Remove forced offline model loading from CI pytest entrypoint and re-run PR checks
