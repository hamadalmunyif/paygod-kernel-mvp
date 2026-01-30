# Output Artifacts (Plan / Findings / Truth Ledger)

Paygod Kernel supports a deterministic compliance loop:

1. **Plan**: what will be evaluated (inputs, pinned packs, digests)
2. **Findings**: signals for triage (flags), references-only evidence pointers
3. **Truth Ledger**: append-only proof log of final decisions (allow/deny/error)

See `contracts/schemas/*` for the canonical JSON Schemas.
