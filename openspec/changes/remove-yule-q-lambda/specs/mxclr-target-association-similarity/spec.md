## REMOVED Requirements

### Requirement: MXCLR target association similarity must support corrected Yule's Q

**Reason**: `yule_q_lambda` is being removed from the MXCLR experiment surface, so NPMI-aware aggregation must no longer support a Yule's Q beta term.

**Migration**: Use the existing cosine/NPMI target similarity blend without a Yule's Q contribution. Remove `yule_q_lambda` from configs and constructor calls.
