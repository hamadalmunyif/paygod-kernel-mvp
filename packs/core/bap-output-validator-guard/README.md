# bap-output-validator-guard (Core)

## Role
This pack is the strict teacher of Belloop Artifact Protocol (BAP).
It defines what is allowed to exist as a PayGod artifact.


## Quick Start (Windows PowerShell)

This repo includes a local validator script that enforces the BAP "Three Gates" rules and returns machine-readable JSON.

### 1) Allow script execution (current session only)
PowerShell may block running local scripts by default. Use **Process** scope to avoid changing your system policy:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
```

### 2) Validate the example vectors (pass + fail)

```powershell
.\tools\bap_validate.ps1 -InputPath "packs/core/bap-output-validator-guard/examples/pass.decision.json"
.\tools\bap_validate.ps1 -InputPath "packs/core/bap-output-validator-guard/examples/pass.evidence.json"

# Expected failures:
.\tools\bap_validate.ps1 -InputPath "packs/core/bap-output-validator-guard/examples/fail.evidence_raw_payload.json"
.\tools\bap_validate.ps1 -InputPath "packs/core/bap-output-validator-guard/examples/fail.bad_schema_version.json"
```

### Output contract
The validator prints JSON:
- ok: true/false
- message: success message (when ok=true)
- code: reason code (when ok=false)
- optional errors[] (schema validation details)

Examples:
- Gate 1: ENV_SCHEMA_VERSION_INVALID, ENV_SCHEMA_REF_MISSING
- Gate 3: REF_RAW_CONTENT_DETECTED


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
