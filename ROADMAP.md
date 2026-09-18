# Roadmap

This roadmap separates **proven repository witnesses** from future product claims.

## Proven baseline
- **v0.1 Deterministic contracts/execution:** schemas, fixtures, deterministic pack execution, CI gates.
- **v0.2 Evidence/ledger/receipt:** schema-governed artifacts, hash chaining, manifest and receipt binding.
- **v0.3 Portable evidence:** artifact-only handoff, cross-environment/cross-OS verification, tamper rejection.
- **v0.4 Standalone verifier witness:** versioned verifier artifact in CI, no repository checkout, no pack replay, clean -> VALID, tamper -> INVALID.

## Next gates

### v0.5 — External distribution + trust boundary
Package/distribute verifier v0.1.0 outside producer-repository context and record an external-device/party witness.

### v0.6 — Evidence Provenance Contract
Bind source identifier, issuer identity, observation/retrieval and validity time, signature/API attestation or equivalent source proof, and payload digest.

### v0.7 — First real domain pack
One bounded Conditional Invoice Release Pack: evidence + policy + facility state -> RELEASE / REDUCE / HOLD, preserving kernel semantics.

### v0.8 — Shadow pilot
Run 20–50 real cases against human decisions. Measure decision time, missing evidence, exceptions, overrides, and audit reconstruction. Stop generic feature development during this gate.

### v0.9 — Conditional-release pilot
Integrate a downstream execution rail only after shadow-pilot evidence. Human approval may remain in the loop initially.

## Deferred
Metrics expansion, OSCAL/profile expansion, tokenization, agent-payment rails, Open Banking aggregation, AI underwriting, large dashboards, and additional domain platforms are not commitments until a real pilot demonstrates the need.
