# bap-output-validator-guard (Core)

## Role
This pack is the strict teacher of Belloop Artifact Protocol (BAP).
It defines what is allowed to exist as a PayGod artifact.

## What it enforces (MVP)
- Envelope is mandatory
- Schema binding is explicit (no guessing)
- Evidence & ledger_entry are references-only
- schema_version must be strict SemVer
- Allowed kinds: decision, evidence, ledger_entry

## Outputs (MVP)
- decision: pass/fail + reason codes (no sensitive payloads)
- evidence: references-only proof (refs, hashes, metadata)
- ledger_entry: append-only reference record (hash-chained)

## Non-goals (MVP)
- No raw content storage
- No PII handling
- No provider logic
- No APIs / Docker

## Authority
This pack is normative. If an artifact fails here, it is not considered system truth.
