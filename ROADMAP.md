# Roadmap

This roadmap separates proven repository capabilities from rehearsal evidence, external-pilot evidence, and future product claims.

## Proven baseline

### v0.1 — Deterministic contracts and execution — PROVEN
- canonical schemas and fixtures;
- deterministic execution witness;
- contract validation;
- CI gates.

### v0.2 — Evidence, ledger, and receipt binding — PROVEN
- schema-governed evidence artifacts;
- ledger append/verification and hash chaining;
- manifest and bundle-digest binding.

### v0.3 — Portable evidence verification — PROVEN IN CI
- artifact-only producer -> verifier handoff;
- Linux producer -> Windows verifier;
- no replay required for integrity verification;
- one-byte tamper rejection.

### v0.4 — Standalone/no-checkout verifier witness — PROVEN IN CI
- versioned standalone verifier artifact;
- recipient jobs do not check out the repository;
- manifest-locked ledger and decision-critical receipt binding;
- fail-closed malformed/tamper witnesses.

### v0.5.1 — Verification Contract Repair — PROVEN
- restricted `paygod-c14n-v1`;
- safe integers only;
- cross-runtime fail-closed parity;
- scoped verification dimensions;
- external receipt commitment;
- verified ledger head;
- strict transferred-member contract;
- manual production-browser receipt-pin witness.

## Current gate

### v0.5.2 — Minimal Issuer Authentication
Goal: authenticate the receipt commitment without confusing key authentication with external truth.

- optional detached `receipt.sig.json`;
- Ed25519 only;
- domain-separated signed message;
- external recipient trust store;
- `verified | not_verified | failed` issuer-authentication states;
- RFC 8032 regression vector;
- private key remains outside the repository;
- no claim of regulator authorization, source truth, replay, or trusted time.

## Next gate

### v0.6 — Internal Rehearsal B2
This is **not a pilot** and does not prove demand or willingness to pay.

Run one bounded decision workflow against:
- real/de-identified historical cases where available;
- blind/synthetic cases prepared independently;
- adversarial/tamper cases;
- a simple checklist/spreadsheet baseline;
- relevant open-source/standards reference implementations where useful.

Measure:
- human/Paygod agreement and disagreement causes;
- evidence gaps;
- preparation and audit time;
- false INVALID rate across implementations;
- adversarial tamper rejection;
- whether a non-developer can explain what was and was not verified.

Exit artifact: one-page Internal Rehearsal Readiness Report.

### v0.7 — Workflow-derived provenance contract
Only after rehearsal evidence:
- define the minimum real evidence sources;
- source/issuer identifiers;
- observation and validity time;
- payload commitments;
- source attestations/signatures where actually available.

### v0.8 — External shadow pilot
Only with a real design partner:
- 20–50 real decisions;
- Paygod does not autonomously move money;
- compare Paygod output to actual human decisions;
- measure missing evidence, exceptions, overrides, reconstruction time, and operational value.

### v0.9 — Conditional release integration
Only after external-pilot evidence supports it:
- downstream approval/execution rail;
- pre-flight release evidence;
- post-flight conformance evidence where required.

## Watch / paused

Do not expand generic metrics, OSCAL/profile breadth, tokenization, agent-payment rails, Open Banking aggregation, AI underwriting, large dashboards, new container formats, or domain packs merely because they are technically possible.

Build work requires a named accumulation point for value after success.
