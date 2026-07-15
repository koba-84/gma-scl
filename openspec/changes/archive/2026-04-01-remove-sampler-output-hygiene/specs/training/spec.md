## REMOVED Requirements

### Requirement: Sampler runtime output hygiene

**Reason**: sampler runtime の stdout cleanliness は研究システムの再現性・データ契約・学習挙動を表す requirement ではなく、implementation hygiene に近いため main spec で維持しない。

**Migration**: sampler の system-level regression は `tests/test_data_integration.py` の sampler switching / initialization / reproducibility で継続確認する。stdout cleanliness に依存した targeted pytest は削除する。
