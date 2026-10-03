# Internal Verification Challenge v0.1

Status: engineering rehearsal after v0.5.1. **This is not an external pilot.**

## Purpose

Pressure-test the verification contract before selecting a real partner workflow. The challenge is intentionally small and adversarial: it should reveal trust-boundary mistakes before a domain pack or partner can hide them.

Run:

```bash
python tools/internal_verification_challenge.py --result internal-verification-challenge-result.json
```

Acceptance requires all five cases to pass.

## Five cases

| Case | What it tests | Expected result |
|---|---|---|
| Clean bundle / scoped claims | A clean, externally pinned receipt reports only what was actually verified | integrity verified; issuer authenticity not verified; replay not performed; producer-supplied time |
| Restricted profile | Float, unsafe integer, non-NFC key, and unpaired surrogate probes | all fail closed |
| Manifested byte mutation | One-byte mutation in a locked artifact | integrity fails |
| Unexpected member | Unmanifested file such as `.DS_Store` | integrity fails |
| Coordinated full rewrite | Ledger + manifest + receipt are coherently re-authored from genesis | unpinned integrity may verify; original external receipt pin MUST reject the replacement |

The fifth case is a required **non-claim witness**. Paygod must not pretend an internally self-consistent bundle proves it is the originally issued bundle. The external receipt commitment is what distinguishes the original bytes from a coherent replacement.

## Reference baselines

These are architectural comparison references. This challenge does **not** claim to execute their implementations.

### Bellbook

Bellbook 0.11 exposes a three-way receipt validation status: `Clean`, `Tainted`, and `Invalid`. Its replay-oriented evidence model is a useful baseline for deciding whether Paygod is adding anything beyond generic replayable evidence.

Reference:
- https://docs.rs/bellbook/latest/bellbook/receipt/enum.ValidationStatus.html

### Evidra / Evidra-Lock

Evidra records operation intent/outcome in signed, tamper-evident evidence and separates verification dimensions such as chain validity, signature validity, and coverage. Evidra-Lock is a useful pre-execution-policy baseline: structured request -> deterministic policy decision -> evidence, with execution elsewhere.

References:
- https://github.com/vitas/evidra
- https://github.com/vitas/evidra-lock

### in-toto Attestation

in-toto separates Predicate, Statement, Envelope, and Bundle. During later domain work, Paygod must ask whether its decision evidence can reuse those layers instead of inventing another generic attestation envelope.

Reference:
- https://github.com/in-toto/attestation/tree/main/spec

### SCITT

RFC 9943 separates issuer-signed statements from Transparency Service registration receipts. It is a baseline for issuer identity, transparency, and external anchoring concepts; Paygod should not relabel generic transparency mechanics as proprietary product differentiation.

Reference:
- https://www.rfc-editor.org/rfc/rfc9943.html

## What this challenge can establish

- the repaired canonicalization profile fails closed on the selected hazards;
- the standalone verifier rejects direct byte tampering and unexpected members;
- the verifier exposes trust dimensions rather than a broad undifferentiated VALID;
- an external receipt commitment detects a coordinated replacement that internal consistency alone cannot distinguish.

## What it cannot establish

- market demand or willingness to pay;
- external evidence truth;
- authorized issuer identity;
- trusted third-party time;
- decision replay;
- fitness for a specific gas, logistics, finance, or industrial workflow.

## Exit gate

Proceed to the 30-case Internal Workflow Rehearsal only when:

1. all five cases pass in CI;
2. no false-INVALID cross-runtime mismatch remains in the covered profile;
3. the coordinated-rewrite case demonstrates the external-root requirement explicitly;
4. documentation and UI do not convert integrity into authenticity, replay, truth, or trusted-time claims.

Failures are classified before code changes as:

`contract gap / domain evidence gap / provenance gap / UX gap / kernel defect`

Only a demonstrated kernel defect justifies changing the kernel.
