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
Every artifact MUST be wrapped in a common envelope:
- kind
- schema
- schema_version
- timestamp
- producer
- correlation_id
- data

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
