# Quasi-Realistic Gas Site Readiness Rehearsal — 2026-10-03

## Classification

`quasi_realistic_simulation`

This is an internal workflow challenge. It does **not** count as a real/de-identified B2 case set and does not establish regulatory compliance, external evidence truth, independent human judgment, or external-pilot readiness.

## Objective

Exercise the frozen Gas Site Readiness workflow with scenarios shaped like operational handover cases rather than arbitrary boolean combinations.

The test intentionally includes both:
- cases fully representable by the current contract; and
- plausible operational facts that the current contract cannot yet represent or authenticate.

## Result

CI run: `37094963300`

- cases executed: **10**
- case-level test passes: **10/10**
- portable evidence integrity verified: **10/10**
- simulated operator / PayGod agreements: **8**
- deliberate disagreements: **2**
- false pipeline failures: **0**

The two disagreements were expected and are the useful result of this rehearsal.

## Case outcomes

| Case | Scenario | Simulated operator | PayGod | Relationship | Classification |
| --- | --- | --- | --- | --- | --- |
| SIM-01 | New restaurant central LPG handover | READY | READY | AGREE | — |
| SIM-02 | Bakery branch after failed pressure test | REJECT | REJECT | AGREE | — |
| SIM-03 | Hotel kitchen with fire-protection work incomplete | REJECT | REJECT | AGREE | — |
| SIM-04 | Required leak shutoff not ready | REJECT | REJECT | AGREE | — |
| SIM-05 | Warning signage incomplete | HOLD | HOLD | AGREE | — |
| SIM-06 | Pre-operation notification evidence absent | HOLD | HOLD | AGREE | — |
| SIM-07 | Leak detection declared not required under the frozen rehearsal policy | READY | READY | AGREE | — |
| SIM-08 | Evidence references another site | REJECT | REJECT | AGREE | — |
| SIM-09 | Pressure test passed, but certificate validity is expired | HOLD | READY | DISAGREE | contract_gap |
| SIM-10 | Detector is declared ready, but calibration/source provenance is unavailable | HOLD | READY | DISAGREE | provenance_gap |

## What SIM-09 exposed

The current contract represents:

`pressure_test_passed: true | false`

It does not represent:
- test date;
- expiry / validity window;
- certificate identifier;
- issuer;
- issuer authenticity.

Therefore a technically passed but operationally expired pressure-test certificate can be flattened to `true`, and the frozen policy returns READY.

This is a **contract gap**, not a kernel defect.

## What SIM-10 exposed

The current contract represents:

`leak_detection_auto_shutoff_ready: true | false`

It does not establish:
- where that assertion came from;
- who issued or measured it;
- detector calibration status;
- calibration validity;
- payload/source commitment.

Therefore the integrity layer can correctly verify the transferred declaration while the underlying provenance remains insufficient.

This is a **provenance gap**, not a kernel defect.

## Architectural interpretation

The rehearsal supports the current product boundary:

```text
evidence declaration
        ↓
deterministic policy
        ↓
decision
        ↓
portable integrity proof
```

But realistic operations need another layer for selected evidence:

```text
source / issuer
        ↓
observation + validity
        ↓
evidence commitment / attestation
        ↓
authority contract
        ↓
decision
        ↓
portable proof
```

This result is evidence for designing the future workflow-derived provenance contract. It is **not** permission to expand the kernel generically.

## Technical timing observation

The CI runner measured per-case production + verification around 286–298 ms after first-run warm-up; SIM-01 was 641 ms. These are engineering-runner observations only and are not operational baseline timings.

## Next use

Use these 10 cases to rehearse:
1. recipient interpretation;
2. signature/trust-store verification;
3. provenance-field design for the two exposed gaps;
4. later replacement by real/de-identified operational cases when available.

The real B2 readiness gate remains unchanged and must continue to report zero real cases until real/de-identified cases are actually collected.
