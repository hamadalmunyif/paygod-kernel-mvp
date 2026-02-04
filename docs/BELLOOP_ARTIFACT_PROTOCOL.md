# Belloop Artifact Protocol (BAP)

## Scope (MVP)
BAP defines the stable, schema-validated artifacts that power Belloop.
In MVP, only three artifact kinds are mandatory:
- decision
- evidence
- ledger_entry

Other artifacts (findings_report, impact, plan_report, measurement, metricspec, observation) are out-of-scope for MVP unless explicitly enabled.

## Source of Truth
The system is governed by validated artifacts (schemas), not by code or services.
Any producer (CLI/service/pack) is interchangeable if it emits compliant artifacts.

## Envelope (Required)
Every artifact MUST be wrapped in a common envelope defined by the canonical schema:

Fields (defined by contract):
- correlation_id
- data
- kind
- producer
- schema
- schema_id
- schema_ref
- schema_version
- timestamp

Required fields (must exist):
- data
- kind
- producer
- schema_version
- timestamp

Notes:
- correlation_id is OPTIONAL in MVP by the current envelope contract (recommended when available).

No envelope => non-compliant output.



## References-only (Security Rule)
Artifacts MUST NOT store raw sensitive content or PII.
- evidence MUST contain references/hashes/ids only.
- ledger_entry MUST be append-only, hash-chained, and references-only.

Raw payloads belong to external storage and must be referenced by hash/uri/id.

## Schema Stability
- Existing schemas are never broken.
- Breaking changes require a new schema version.
- Changes require test vectors and ADRs when architectural.

## Pack Compliance
Every Pack MUST declare:
- inputs consumed
- artifact kinds produced
- supported schema versions
- validation/tests for outputs

## Implemented files
- contracts/schemas/belloop_artifact_envelope.schema.json
- docs/BELLOOP_ARTIFACT_PROTOCOL.md
