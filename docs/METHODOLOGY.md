# TRACE Methodology

TRACE follows a simple evidence model:

1. Acquire or receive evidence without modifying the source where practical.
2. Hash collected evidence using SHA-256.
3. Parse supported artifacts into a common event model.
4. Preserve observed facts as distinct records.
5. Apply deterministic correlation rules.
6. Record the basis for every inferred relationship.
7. Present timelines and graphs for human review.
8. Export a reproducible report with limitations.

Confidence values are prioritization scores, not statistical probabilities. A relationship is not an attribution. A missing artifact does not prove that an event did not occur.

## Correlation examples

- Same filename + close timestamps → possible download-to-file relationship.
- Same URL host + close timestamps → possible browser-to-download relationship.
- Same SHA-256 → byte identity of the examined objects.

Each rule is intentionally transparent so an investigator can inspect why an edge was created.
