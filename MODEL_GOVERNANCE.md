# Pack Model Governance

Policy packs are the main extension surface of Paygod Kernel.
This document defines a stable and auditable lifecycle.

## Lifecycle states

- **Draft**: initial development; may change frequently.
- **Reviewed**: community review completed; tests exist and pass.
- **Verified**: higher assurance; requires maintainers and pinning/signing.
- **Published**: included in releases / registries (if enabled).
- **Activated**: enabled in a given environment (GitOps applies).
- **Retired**: no longer recommended; retained for audit/history.

## Trust levels

### Community
- schema-valid
- has tests (`tests/cases.yaml`)
- deterministic behavior (no non-deterministic inputs)

### Verified
- two maintainer approvals
- pinned dependencies (no floating URLs / branches)
- signed merge commit
- clear evidence requirements (references-only)

## Evidence rules (default)

- **References-only**: packs must not embed PII or sensitive content into ledger entries.
- Findings may include non-sensitive context; evidence content belongs in an evidence store.

## Versioning

- Packs use SemVer.
- A *behavioral change* requires at least a MINOR bump.
- A change in required inputs requires MAJOR bump.

## Retirement

A pack is retired when:
- superseded by a newer pack
- incompatible with current schema/DSL
- known to produce unsafe/incorrect outcomes

Retired packs remain in the repository under `packs/_retired/` with a short reason note.
