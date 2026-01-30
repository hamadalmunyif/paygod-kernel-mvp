# ADR-0001: Separate Truth Ledger from Findings

## Status
Accepted

## Context
Paygod Kernel must provide reproducible proof outputs. Operational signals (e.g. flags) are useful but are not “truth”.

## Decision
- **Truth decisions** are limited to: `allow`, `deny`, `error`.
- **Findings** are emitted separately with `kind=flag|info` and `severity`.
- The **truth ledger** is append-only and contains **references-only** (no PII).

## Consequences
- Ledger remains small and audit-friendly.
- Findings can be routed to ticketing/PR comments without polluting proof history.
