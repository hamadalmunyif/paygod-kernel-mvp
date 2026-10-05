# Repository Stop-Build Rule

Status: ACTIVE  
Effective baseline: `6b65d0d97ce61111b9eb77762de03f4a518c0d21`  
Activated after: P0 closure / PR #92

## Purpose

Stop-build preserves the current canonical decision path while B2-REAL and external validation generate evidence. It is not an incident-response freeze and it does not prohibit evidence collection.

## Frozen development

Without a new evidence-backed governance decision, do not add:

- new kernel features or semantics;
- new policy-DSL semantics;
- new receipt, ledger, canonicalization, or schema semantics;
- new generic trust or security capabilities;
- new execution-authority machinery;
- predecessor-state binding implementation;
- post-flight conformance implementation;
- next-transition eligibility implementation;
- Virtuals-specific logic in the kernel;
- unrelated payment, tokenization, Open Banking, AI-underwriting, dashboard, or domain expansion.

A research hypothesis is not implementation authorization.

## Allowed work

Allowed work is limited to:

1. confirmed defect remediation, including a demonstrated `kernel_defect`;
2. critical vulnerability remediation;
3. CI, build, dependency, or reproducibility repair required to preserve existing witnesses;
4. documentation and evidence records;
5. B2-REAL collection and analysis;
6. external observational validation that does not mutate the kernel merely to make an external case fit;
7. a separately approved architecture change backed by a new witness and explicit ADR/governance record.

## Required sequence

```text
Observe
→ classify
→ count recurrence
→ assess operational importance
→ identify the correct layer
→ decide whether build is justified
→ ADR / explicit governance
→ implementation
```

No step may be skipped because a proposed primitive appears reusable.

## P0 freeze

P0 remains historical evidence:

- `CLOSED — PASS WITH BOUNDARY`;
- `simulated_shadow_pilot`;
- `counts_as_b2_real = false`.

Frozen P0 source records, mapping registers, decision log, and closure report are not rewritten to improve later claims. A material factual correction must be recorded as a dated erratum or superseding record while preserving the original witness.

## B2 and X1

B2-REAL remains open and gating for its own readiness claim.

Virtuals X1 is a separate non-gating external validation track. X1 may challenge the architecture but cannot authorize a kernel change from a single observation.

## Exit from stop-build

Stop-build does not expire by date. A proposed build area may leave stop-build only when the repository records a concrete external/real workflow witness, the observed gap or opportunity, recurrence or sufficient operational importance, why the existing layer is insufficient, the intended layer of change, explicit non-claims, and an approved architecture record.

Until then, the default is: **do not build**.
