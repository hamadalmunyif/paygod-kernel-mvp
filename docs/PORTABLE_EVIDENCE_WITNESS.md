# Portable Evidence Witness

Status: bootstrap for PR #52. This document defines the acceptance test for portable evidence. It does **not** claim portability is proven yet.

## Goal

Prove that Paygod evidence can leave the environment that produced it and be independently verified from transferred artifacts only.

## Required witness

```text
Environment A (producer)
        |
        | execute once
        v
Evidence bundle
        |
        | transfer artifacts only
        v
Environment B (verifier)
        |
        | no producer temp/workspace state
        | no hidden local configuration
        | no re-execution of the original decision
        v
VALID / INVALID
```

## Acceptance criteria

1. Producer generates an evidence bundle containing the existing execution receipt and associated evidence artifacts.
2. Producer uploads only that evidence bundle as a CI artifact.
3. A separate verifier job downloads the artifact and verifies it independently.
4. Verification checks the receipt, manifest/digests, and ledger integrity when a ledger is present.
5. A tamper test modifies at least one byte in a copied artifact and verification MUST fail.
6. Verification emits a machine-readable `verification-result.json`.
7. After artifact-only handoff works, add a cross-OS witness, preferably Linux producer -> Windows verifier.
8. Kernel decision semantics and canonicalization rules remain unchanged.

## Non-goals

- No new business workflow or financing logic.
- No SCR, Open Banking, or agentic-payment integration.
- No claim that PR #51 proved evidence portability.

## Target claim after CI passes

> Paygod evidence survives transfer and can be independently verified outside the environment that produced it.
