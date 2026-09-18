# Paygod Kernel — Architecture Audit

Status: audit baseline after PR #53. This document records the current architecture before any new product or domain expansion.

## Executive finding

The kernel has crossed the portability boundary: deterministic execution, schema-governed evidence, receipt binding, cross-environment artifact handoff, tamper rejection, and a CI-level standalone/no-checkout verifier witness are present.

The next engineering risk is not more kernel capability. It is architectural drift. New domain work MUST enter through contracts, packs, evidence adapters, or explicitly versioned interfaces before changing kernel semantics.

## Canonical trust path

```text
External fact/source
        |
        v
Evidence / provenance
        |
        v
Contract + Policy Pack
        |
        v
Deterministic Kernel
        |
        v
Decision Artifact
        |
        v
Manifest + Receipt + Ledger
        |
        v
Portable Evidence Bundle
        |
        v
Independent Verifier
```

Execution rails (bank, PSP, agent, API) are downstream consumers. They are not part of the kernel trust primitive.

## KEEP

- `src/PayGod.Cli` — canonical CLI entry point.
- `src/Paygod.Contracts` and `contracts/` — schema-governed interfaces and versioning.
- `src/Paygod.ControlEngine` — policy/control evaluation boundary.
- `packs/` — domain/control extension mechanism.
- Ledger primitives — tamper-evident decision history.
- Receipt + manifest binding — portable decision evidence.
- CI contract/security/determinism gates.
- Standalone verifier — independent evidence verification boundary.

## FREEZE

Freeze semantics unless a failing real domain pilot demonstrates a required change:

- canonicalization and digest semantics;
- evidence-bundle digest construction;
- receipt-to-manifest binding;
- ledger hash-chain rules;
- deterministic pack evaluation semantics;
- verifier VALID/INVALID fail-closed behavior;
- no-checkout verification trust boundary.

A domain feature alone is not sufficient justification to modify these primitives.

## REVIEW / DEPRECATE CANDIDATES

These are not marked for deletion. They require justification against the current product thesis before expansion:

- Metrics service: do not expand until a domain pilot requires measurement semantics.
- OSCAL/control-profile roadmap work: pause unless demanded by a concrete institutional workflow.
- Demo/bootstrap APIs: keep only as adapters; they MUST NOT become an alternate decision implementation.
- Historical documentation and stale roadmap language that predates portable/standalone verification.
- Old open documentation PRs should be reconciled against current `main`, not merged mechanically.

## MISSING

### 1. External distribution witness
The standalone verifier has a CI-level no-checkout witness. A packaged, versioned verifier still needs an external-device/party witness outside the repository CI context.

### 2. Evidence provenance
Integrity is not provenance. The current verifier can prove that evidence used by a decision has not changed; it does not by itself prove that an external fact is true or that a claimed issuer supplied it.

Minimum provenance contract should eventually bind:
- source identifier;
- issuer identity;
- retrieval/observation time;
- validity time where applicable;
- signature/API attestation or equivalent source proof;
- payload digest.

### 3. Issuer authenticity / trust root
Receipt integrity must eventually be complemented by an explicit issuer identity/signing and key-rotation model before relying parties treat a receipt as an authenticated institutional assertion.

### 4. Real domain authority pack
No current pack proves a production financial release workflow. A first bounded pack should model a real workflow without changing kernel semantics.

Candidate:
```text
invoice + PO + facility state + collateral/evidence + policy
                         |
                         v
              RELEASE / REDUCE / HOLD
                         |
                         v
                       receipt
```

### 5. Real institutional witness
A shadow pilot must compare Paygod output with actual human decisions before Paygod is allowed to control money movement.

## Architectural invariants

1. One canonical decision path. APIs are adapters, not alternate engines.
2. Separate FACT, EVIDENCE, POLICY, DECISION, and EXECUTION.
3. Domain logic belongs in packs/adapters before kernel changes.
4. Verification must not require replay of the original decision.
5. Verification must fail closed on mutation or missing required bindings.
6. Hosting is not a trust root. A future web verifier must preserve offline/independent verification semantics.
7. Do not claim external truth merely because bundle integrity verifies.

## Stop-build rule

After the first real domain pack is implemented, stop generic feature development and run a shadow pilot.

Do not add tokenization, agent-payment rails, an Open Banking aggregator, AI underwriting, a large dashboard, or domain-specific platform features until evidence from a real workflow shows they are necessary.

## Proposed sequence

1. Align README, START_HERE, ROADMAP, GATES, and verifier documentation with the architecture actually on `main`.
2. Declare the kernel invariants/freeze boundary.
3. Package verifier v0.1.0 and run an external portability witness.
4. Define Evidence Provenance Contract v0.1.
5. Implement one Conditional Invoice Release Pack v0.1.
6. Stop coding and run a 20–50 case shadow pilot.
7. Only after measured value, test conditional release into a downstream execution rail.

## README rule

`README.md` is the public entry point and MUST be updated whenever a merged architectural change materially changes:
- what Paygod is;
- what has been proven;
- the canonical execution/trust path;
- required CI gates;
- the next supported developer workflow.

The README must distinguish proven guarantees from roadmap claims.

## Current non-claims

The repository does not yet prove:
- external real-world evidence truth;
- a published/signed external verifier trust root;
- a live bank/PSP release integration;
- autonomous authority over money movement;
- institutional adoption or willingness to pay.

Those are future gates, not current guarantees.
