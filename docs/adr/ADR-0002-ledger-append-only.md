# ADR 0002: Immutable Ledger Strategy

## Status
Accepted

## Context
Financial and regulatory systems (like Paygod) operate under strict audit requirements (OSCAL, SOC2). A traditional CRUD (Create, Read, Update, Delete) database model is insufficient because it allows history to be rewritten or deleted, destroying the audit trail.

We need a storage strategy that guarantees:
1. **Non-repudiation**: Once an action is recorded, it cannot be denied.
2. **Traceability**: The full history of an entity is preserved.
3. **Tamper-Evidence**: Any attempt to alter past records is detectable.

## Decision
We will implement an **Append-Only Immutable Ledger** as the authoritative data store for all decisions and assessments.

### Key Characteristics:
1. **No UPDATE/DELETE**: The database user for the application will strictly lack `UPDATE` and `DELETE` permissions on ledger tables.
2. **Cryptographic Chaining**: Each record will include a hash of the previous record (`PrevHash`), forming a Merkle-like chain.
3. **Corrections as Append**: Modifications are modeled as new "Correction" records that reference the original record ID.

## Consequences

### Positive
- **Audit-Ready**: The system is compliant by design. Auditors can verify the integrity of the chain.
- **Debuggability**: We can reconstruct the exact state of the system at any point in time.
- **Simpler Concurrency**: Append-only writes reduce lock contention compared to complex updates.

### Negative
- **Storage Growth**: Database size will grow monotonically. Archival strategies will be needed for very old data.
- **Query Complexity**: Fetching the "current state" requires aggregating the history or maintaining a separate "Read Model" (CQRS).
- **GDPR/Privacy**: "Right to be Forgotten" is challenging; we must use "Crypto-shredding" (deleting the encryption key) or store PII off-ledger.

## Compliance
This decision supports **Axiom 2: Ledger Immutability**.

## References
- [NIST SP 800-53 (AU-9 Protection of Audit Information)](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
