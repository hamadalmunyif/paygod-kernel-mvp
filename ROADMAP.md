# Roadmap

This roadmap distinguishes **proven repository capabilities** from future product claims.

## Proven baseline

### v0.1 — Deterministic contracts and execution — PROVEN
- canonical schemas and fixtures;
- deterministic execution witness;
- contract validation;
- CI gates.

### v0.2 — Evidence, ledger, and receipt binding — PROVEN
- schema-governed evidence artifacts;
- ledger append/verification and hash chaining;
- manifest and bundle-digest binding;
- deterministic receipt artifact under the injected-clock witness; the supported non-strict local path does not claim deterministic-time binding.

### v0.3 — Portable evidence verification — PROVEN IN CI
- artifact-only producer -> verifier handoff;
- Linux producer -> Windows verifier;
- no replay of the original decision;
- one-byte tamper rejection.

### v0.4 — Standalone/no-checkout verifier witness — PROVEN IN CI
- versioned standalone verifier artifact;
- recipient jobs do not check out the repository;
- clean evidence -> VALID;
- payload and decision-critical receipt tamper -> INVALID;
- exactly one manifest-locked decision ledger is required;
- malformed control data -> machine-readable INVALID;
- Unicode ledger canonicalization parity is regression-tested;
- supported default-clock output remains verifiable only through explicit `--allow-unbound-clock` opt-in and is labeled as unbound; silent strict-to-unbound downgrade is rejected.

## Next gates

### v0.5 — External verifier distribution and witness — NEXT
- package a versioned verifier outside repository CI;
- publish integrity/version metadata;
- verify clean evidence on an independent external device/environment;
- demonstrate external tamper rejection.

### v0.6 — Evidence Provenance Contract v0.1
Bind source identifier, issuer identity, retrieval/observation time, validity time where applicable, source attestation/signature where available, and payload digest.

Integrity alone must not be presented as proof of external truth.

### v0.7 — First real domain authority pack
Candidate: Conditional Invoice Release Pack v0.1.

```text
RELEASE / REDUCE / HOLD
```

Domain logic belongs in a pack/adapter before kernel changes.

### v0.8 — Shadow institutional pilot
- 20–50 real cases;
- Paygod does not move money;
- compare Paygod decisions with actual human decisions;
- measure decision time, missing evidence, exceptions, overrides, and audit reconstruction.

### v0.9 — Conditional release integration
Only after shadow-pilot evidence supports it:
- downstream human approval and/or execution rail;
- pre-flight release receipt;
- post-flight conformance evidence where applicable.

## Paused until demanded by evidence
Do not expand generic Metrics, OSCAL/profiles, tokenization, agent-payment rails, Open Banking aggregation, AI underwriting, or large dashboards merely because they appeared on an older roadmap.
