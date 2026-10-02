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
- manifest/file integrity and decision-critical receipt/ledger binding;
- malformed control data -> machine-readable failure;
- explicit handling of the supported unbound-clock mode.

The v0.4 witness proved useful mechanics but used a broader `VALID` label and an inaccurate `rfc8785` declaration. Those are contract defects, not guarantees to preserve.

## Current gate

### v0.5.1 — Verification Contract Repair
Issue: #67

Required before any workflow rehearsal:
- replace the inaccurate `rfc8785` claim with the restricted `paygod-c14n-v1` profile;
- safe integers only; reject floats/decimals/exponent numbers and unsafe integers;
- require NFC object/property names while preserving string values without silent normalization;
- fail closed on unsupported values;
- keep C# producer and Python verifier aligned on shared acceptance/rejection vectors;
- expose independent verification dimensions: integrity, issuer authenticity, replay, and time authority;
- emit `receipt_sha256` and accept `--expect-receipt-sha256`;
- emit verified `ledger_head`;
- reject unexpected transferred files/symlinks.

This gate does **not** add issuer signing, trusted time, replay execution, a new container format, or a domain pack.

## Readiness sequence

### v0.5.2 — Internal Verification Challenge
Not a pilot.

- attack the verifier/profile with malformed, Unicode, unsafe-number, mutation, receipt-pin, and cross-runtime cases;
- benchmark the evidence/receipt mechanics against relevant open implementations and standards where useful;
- record failures by class: contract gap, provenance gap, UX gap, domain gap, or kernel defect;
- do not expand the kernel merely to make a benchmark pass.

### v0.6 — Internal Workflow Rehearsal
Not a market/adoption claim.

- one bounded decision workflow;
- approximately 30 cases from real/de-identified experience, blind/synthetic cases, and adversarial cases;
- human decision captured before Paygod output;
- baseline comparison with a signed checklist/spreadsheet;
- measure false INVALID, tamper detection, evidence preparation cost, reconstruction time, and recipient understanding;
- produce a one-page readiness report.

Exit requires a clean engineering story; it does **not** prove demand or willingness to pay.

### v0.7 — Design-partner discovery and derived provenance
Only after internal readiness:
- identify an actual decision owner and recurring workflow;
- learn the real evidence sources and missing-evidence rules;
- derive the minimum provenance contract from those sources rather than inventing it in advance.

### v0.8 — Shadow external pilot
- 20–50 real cases where practical;
- Paygod does not move money or perform the controlled action;
- compare Paygod decisions with actual human decisions;
- measure exceptions, overrides, missing evidence, decision time, and audit reconstruction.

### v0.9 — Authenticated issuer / optional replay / conditional release
Only when demanded by the real workflow:
- issuer signing/key-rotation profile;
- replay only when input, policy, runner identity/digest, clock and other deterministic material are actually carried;
- downstream human approval and/or execution rail;
- pre-flight release receipt and post-flight conformance evidence where applicable.

## Paused until demanded by evidence

Do not expand generic Metrics, OSCAL/profiles, tokenization, agent-payment rails, Open Banking aggregation, AI underwriting, large dashboards, or new archive/container formats merely because they are technically possible.

**Build only what has a known accumulation path after success.**
