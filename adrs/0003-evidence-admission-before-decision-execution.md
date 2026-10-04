# ADR 0003 — Evidence Admission Before Decision Execution

Status: Accepted
Date: 2026-10-05

## Context

The Gas Site Readiness P0 workflow exposed a boundary that the frozen boolean contract cannot safely resolve by itself.

Historical source material may be missing, temporally UNPROVEN, semantically weaker than a frozen field, or outside the representable contract. Converting those conditions to false merely to execute the kernel would collapse distinct states:

missing evidence ≠ negative evidence ≠ known unsafe condition.

The repository's external diagnostic challenges also reinforce the need to avoid forcing facts into approximate frozen fields. Those challenges do not by themselves authorize a kernel change.

## Decision

PayGod workflows that depend on external evidence SHALL perform evidence admission before canonical decision execution.

The pre-kernel sequence is:

Claim / Source Evidence
→ Semantic Representability
→ Historical / Provenance Admission
→ TRUE | FALSE | WITHHELD
→ Executability Gate
→ Canonical PayGod Decision Path.

Rules:

1. TRUE and FALSE are assigned only when admitted evidence directly supports the frozen field semantics.
2. Evidence that is missing, temporally UNPROVEN, semantically insufficient, or unrepresentable is not silently coerced into FALSE.
3. WITHHELD is a workflow/admission state outside the kernel contract.
4. If a required frozen input remains WITHHELD, the workflow returns NOT RUN before invoking the kernel.
5. NOT RUN is an orchestration result, not a kernel verdict and not READY/HOLD/REJECT.
6. Only an executable complete frozen input enters the existing canonical decision path.
7. This ADR does not add UNKNOWN or tri-state semantics to the kernel, policy DSL, ledger, receipt schema, or Gas Site Readiness pack.

## Consequences

The decision preserves a single canonical kernel path while allowing the surrounding evidence workflow to refuse unsafe semantic coercion.

Real or simulated cases may therefore be valid observations yet remain non-executable.

Human-vs-PayGod agreement is undefined for NOT RUN cases because no PayGod decision exists.

Evidence-admission failures remain diagnostic observations until recurrence and operational importance justify a separate architecture decision.

## Non-decisions

This ADR does not accept or implement:

- predecessor-state binding as a kernel primitive;
- post-flight conformance;
- next-transition eligibility;
- protocol-independent authority;
- automatic contract expansion from an observed gap.

Those remain future hypotheses requiring independent evidence.

## Evidence record

The immediate witness is P0 — Gas Maintenance Workflow & Evidence-Admission Pilot, recorded under rehearsals/gas-site-readiness/p0-maintenance-workflow/.

P0 is simulated and contributes zero cases to B2-REAL.
