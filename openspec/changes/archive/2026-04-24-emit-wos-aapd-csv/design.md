## Design

WoS rows are first normalized into the existing in-memory shape:

- `doc_token`: cleaned abstract text
- `doc_label`: `[domain, area]`

The CSV label space is derived deterministically from first appearance over `doc_label` values in the full dataset. Each split row uses the cleaned abstract as the `abstract` column and writes `1.0` for labels present in `doc_label`, otherwise `0.0`.

This preserves the prior per-row label information while matching AAPD's file contract. The split algorithm keeps the existing NumPy shuffle and sklearn `train_test_split` calls so row membership remains deterministic for the same source workbook.
