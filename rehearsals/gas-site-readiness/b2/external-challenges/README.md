# B2 External Challenge Corpus

This directory contains **non-gating diagnostic challenges** used to stress the frozen Gas Site Readiness evidence boundary.

These files do not count toward the B2 minimum of 10 real/de-identified operational cases.

## Classes

- `B2-EXT-*` — public historical evidence from independent external investigations or records.
- `B2-SENSOR-*` — public technical, sensor, telemetry, or prototype material used to test software-to-physical evidence boundaries.

## Rules

1. External challenges MUST NOT be counted as `B2-REAL-*`.
2. Public source material MUST be pinned or otherwise bound as precisely as the source permits.
3. Observed facts MUST be separated from interpretations and from facts not established by the source.
4. Historical material MUST distinguish contemporaneous evidence from post-incident findings.
5. A challenge MUST NOT coerce an external fact into a frozen B2 field merely to make PayGod executable.
6. A discovered gap does not authorize a kernel change.
7. Third-party secrets, credentials, or sensitive values MUST NOT be copied into this repository.
8. External challenges are diagnostic evidence only; they do not establish market demand, regulatory approval, source truth, or production authority.

The purpose is falsification and boundary discovery: **observe, classify, count recurrence, then decide whether architecture work is justified.**
