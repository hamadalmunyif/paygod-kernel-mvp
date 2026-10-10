# Runtime Ledger Profile — Historical Phase 2 Note

Status: **HISTORICAL TOOLING PROFILE; NOT A PRODUCTION STORAGE OR TRUST GUARANTEE** (reconciled 2026-10-10).

This page previously described an optional local `PAYGOD_LEDGER_PATH` output and an old PowerShell append-helper flow. It is retained as historical operational context; it is not a normative format for canonical decision-bundle identity and not proof of a production append-only/WORM service.

For supported portable evidence semantics use:
- [Kernel README](../README.md)
- [Current architecture](02_ARCHITECTURE.md)
- [Standalone verifier](STANDALONE_VERIFIER.md)
- [GATES](../GATES.md)

## Historical concept

Local scripts may be able to append one JSONL metadata entry per run to a user-selected local path, where each entry contains only record identifiers and digests. Such metadata is a local diagnostic convenience. A timestamp from a local file is **producer supplied**, not trusted third-party time. The local file can be deleted or replaced; it is not a cryptographically immutable audit vault.

The original phase-2 example was not a completed, tested cross-platform quickstart and contained malformed PowerShell snippets. Do not copy that example into production runbooks or rely on it as current setup instructions.

Any durable ledger service, secure retention SLA, and independent timestamp/issuer chain require separate implementation and testing. A coordinated full rewrite of internally valid bundle artifacts requires an external receipt commitment to distinguish replacements.
