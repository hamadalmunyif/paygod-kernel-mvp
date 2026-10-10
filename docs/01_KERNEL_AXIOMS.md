# PayGod Kernel — Implemented Invariants and Unproven Aspirations

Status: **RECONCILED WITH CURRENT README** (2026-10-10).

Earlier versions of this document described all requests as JWT/mTLS-authenticated, WORM ledger storage, universal encrypted service mesh, production panic switches and compliance certifications. Those were proposed architectural requirements, **not capabilities established in the current repository**. Do not market those statements as enforced axioms.

The executable baseline remains the [Kernel README](../README.md), [Architecture Audit](ARCHITECTURE_AUDIT.md), [GATES](../GATES.md), and the frozen [Stop-Build Rule](STOP_BUILD_RULE.md).

## Enforced and witnessed within their stated scope

### 1. Versioned contracts and supported canonicalization

Inputs, artifacts and packs must respect their applicable schemas and the versioned `paygod-c14n-v1` profile. The canonicalization profile rejects fractional/exponent JSON numbers, unsafe integers, and non-NFC property names. Data invalid under that profile must fail closed rather than silently change representation.

A schema describes structure; it does **not** prove source truth, sender mandate, or factual completeness.

### 2. One canonical decision and artifact authority

The canonical Kernel originates decision/artifact/receipt/bundle-identity semantics. **Registered** hosted adapters can invoke or transport but cannot originate alternate decision truth. [Boundary mutation witness](REPOSITORY_BOUNDARY.md) limits this to actual adapters registered in `tools/check_repository_boundary.py`, not every possible plugin.

### 3. Tamper-evident evidence is not immutable physical storage

The exported evidence bundle contains hash commitments, a manifest-locked ledger and receipt bindings that are independently checkable within the verifier contract. These checks detect tested mutations; they do **not** ensure WORM/S3 retention, prevent a coordinated full rewrite absent an independent receipt commitment, or certify a durable enterprise audit vault.

### 4. Independent verification must remain scoped

The standalone verifier can check transferred files without producer runtime/pack replay. Optional detached Ed25519 receipt authentication depends on the recipient's independent trust store. Integrity `verified` does not imply authentic source data, authorization to act, trusted external time, or correct original policy evaluation.

### 5. Missing/unrepresentable evidence must not be coerced

[ADR 0003](../adrs/0003-evidence-admission-before-decision-execution.md) requires admission before Kernel evaluation. `WITHHELD` and `NOT RUN` are **orchestration states outside the Kernel**. They are not new policy-DSL truth values.

### 6. Preserve test and claim boundaries

CI, signed commitments, negative tests, deterministic output and schema checks are different witnesses; none should be promoted into universal guarantees. A tested local controlled-release harness does not establish independent production release authority. Research promotion is recorded in [the transfer register](OBSERVATORY_TRANSFER_ACCEPTANCE_2026-10-10.md).

## Aspirations requiring separate implementation evidence

The following are **not** enforced by the current core merely because they appeared in historical architecture drafts:

- mTLS/JWT on every request, organization identity federation or SSO.
- WORM/immutable retention guarantees on an external cloud ledger.
- production HSM or remote signing, third-party trusted time.
- globally effective panic/kill switches or circuit breakers.
- SOC 2, OSCAL, ISO, HIPAA, FedRAMP or government certification.
- automated financial execution and non-bypassable external enforcers.
- multi-service HA/SLO commitments.

Any new invariant requires a precise implementation contract, a counterexample and falsifiable tests under the current governance process. “Must be true in the future” is not “already proven in code.”
