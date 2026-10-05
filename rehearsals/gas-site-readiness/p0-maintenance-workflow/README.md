# P0 — Gas Maintenance Workflow & Evidence-Admission Pilot

Status: CLOSED — PASS WITH BOUNDARY
Classification: simulated_shadow_pilot
External pilot: false
Counts as B2-REAL: false
Repository baseline used for mapping: 5f680d8c1d2aa6d1290e03ed0501c390c050175d

## Purpose

P0 exercised the human and evidence workflow around the frozen Gas Site Readiness contract without claiming real historical operational evidence.

The exercised path was:

custodian evidence capture
→ historical cut-off
→ independent reviewer judgment
→ judgment freeze
→ frozen-field semantic mapping
→ evidence admission
→ Executability Gate
→ RUN or NOT RUN.

The purpose was to test whether the workflow could preserve uncertainty and stop before the kernel rather than inventing boolean values.

## Frozen inputs

The source custodian intake, reviewer report, and detailed mapping artifact remain frozen outside the public repository. Their filenames and SHA-256 commitments are recorded in ARTIFACT_MANIFEST.json.

The source records are not rewritten retrospectively. P0 defects are preserved as observations rather than repaired by changing the original employee/reviewer records.

## Result

Reviewer outcomes across the 15 simulated cases:

- READY: 0
- HOLD: 9
- REJECT: 6

Strict mapping/admission result:

- executable: 0 / 15
- PayGod RUN: 0 / 15
- PayGod NOT RUN: 15 / 15
- formal human-vs-PayGod disagreements: N/A

The decisive repeated boundary was leak_detection_required = WITHHELD in 15 / 15 cases. No qualifying FALSE assignments were observed in the P0 mapping.

A NOT RUN result is valid when a complete frozen input cannot be constructed without inference or semantic coercion.

## What P0 established

P0 supports these workflow conclusions:

1. missing evidence is not negative evidence;
2. UNPROVEN timing is not false;
3. unrepresentable evidence must not be forced into an approximate field;
4. WITHHELD is a pre-kernel admission state, not a kernel boolean;
5. NOT RUN is a pre-kernel orchestration result, not REJECT;
6. Case Evidence, Professional/Normative Knowledge, Decision Semantics, and Kernel Decision are distinct records;
7. a case that does not pass the Executability Gate must not be run merely to manufacture a comparison.

These boundaries are captured narrowly in ADR 0003.

## What P0 did not establish

P0 does not establish:

- 15 real historical cases;
- B2-REAL readiness;
- regulatory compliance;
- external evidence truth;
- production issuer authority;
- commercial adoption;
- a kernel defect;
- a requirement for tri-state kernel semantics;
- post-flight conformance or next-transition eligibility.

## Relationship to B1 and B2

B1 remains the synthetic executable engineering witness.

P0 is a separate simulated workflow/evidence-admission witness.

B2-REAL remains open and unchanged at 0 / 10 qualifying real/de-identified cases.

The kernel and frozen Gas Site Readiness pack remain unchanged.
