# BAP Output Validator Guard â€” Specification (Tutorial + Normative, MVP)

## Status
**Normative** for PayGodCloud-Belloop MVP.
This document defines the minimum rules that decide whether an artifact is allowed to exist as "system truth".

If an artifact fails these rules:
- it MUST NOT be accepted as a PayGod artifact,
- it MUST NOT be written to any truth ledger,
- and it MUST NOT be used to trigger automation.

---

## Purpose (Why this pack exists)
This pack is the strict teacher of the Belloop Artifact Protocol (BAP).

It enforces *contract integrity*:
- No artifact without an explicit contract (JSON Schema)
- No meaning without schema binding
- No safety without references-only for sensitive artifact types

This pack does **not** judge business correctness.
It judges: **Is this artifact allowed to exist here?**

---

## MVP Artifact Kinds (Only)
MVP allows exactly three artifact kinds:

- `decision`
- `evidence`
- `ledger_entry`

Anything else is **Post-MVP** and MUST be rejected until explicitly added via schema + ADR.

---

## Validation Model (Three Gates)

### Gate 1 â€” Envelope Gate (Existence)
All artifacts MUST be wrapped in the envelope schema:

- `contracts/schemas/belloop_artifact_envelope.schema.json`

Required envelope checks:

1) `kind` MUST be one of: `decision`, `evidence`, `ledger_entry`
2) `schema_version` MUST be strict SemVer: `MAJOR.MINOR.PATCH`
3) Either `schema_ref` (preferred) OR legacy `schema` OR legacy `schema_id` MUST exist
4) `timestamp` MUST be RFC3339 date-time
5) `producer` MUST exist with:
   - `producer.name`
   - `producer.version`
6) `correlation_id` is OPTIONAL in MVP (recommended for distributed operation)

**Reason codes (Gate 1):**
- `ENV_MISSING`
- `ENV_KIND_INVALID`
- `ENV_SCHEMA_REF_MISSING`
- `ENV_SCHEMA_VERSION_INVALID`
- `ENV_TIMESTAMP_INVALID`
- `ENV_PRODUCER_INVALID`

---

### Gate 2 â€” Schema Binding Gate (Meaning)
After the envelope is accepted, the validator MUST bind `data` to an explicit schema.

Rules:
- No guessing and no implicit resolution.
- `kind` MUST map deterministically to the correct payload schema.
- `data` MUST validate against that schema.

MVP kind â†’ payload schema mapping:
- `decision` â†’ `contracts/schemas/decision.schema.json`
- `evidence` â†’ `contracts/schemas/evidence.schema.json`
- `ledger_entry` â†’ `contracts/schemas/ledger_entry.schema.json`

**Reason codes (Gate 2):**
- `SCHEMA_NOT_FOUND`
- `SCHEMA_VERSION_UNSUPPORTED`
- `SCHEMA_VALIDATION_FAILED`

---

### Gate 3 â€” References-only Gate (Safety)
For `evidence` and `ledger_entry` artifacts:

- Raw content MUST NOT be stored inside the artifact.
- Only references are allowed (hashes, IDs, URIs, minimal metadata).

This is mandatory because raw content creates:
- security risk,
- legal/PII risk,
- and breaks the principle of stable truth via references.

**Reason codes (Gate 3):**
- `REF_RAW_CONTENT_DETECTED`
- `REF_PII_RISK_DETECTED`
- `REF_UNBOUNDED_PAYLOAD`

---

## Outputs of the Validator (MVP)
This pack defines that validation produces three artifacts:

1) **decision**
   - pass/fail
   - reason codes
   - MUST NOT include sensitive payloads

2) **evidence**
   - references-only proof: refs + hashes + minimal metadata

3) **ledger_entry**
   - append-only record of the validation (hash-chained reference)

All outputs MUST themselves be wrapped by the BAP envelope.

---

## Non-Goals (MVP)
- No storage integration
- No provider-specific logic
- No API design
- No Docker execution
- No business correctness decisions
- No expansion of artifact kinds beyond MVP

---

## Change Control
Any change to these rules or artifact kinds requires:
- schema update (if applicable),
- SemVer policy (no breaking changes without MAJOR),
- and an ADR describing the reason and compatibility impact.
