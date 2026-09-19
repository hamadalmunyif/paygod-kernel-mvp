# Repository Boundary Closure v0.1

Status: proposed architecture gate. This document defines the witness required before Paygod may claim Proof of Single Authority.

## Purpose

This gate proves that Paygod has one execution authority. It does not forbid multiple APIs, cloud services, or adapters. It forbids any non-canonical component from originating independent execution truth.

## Trust invariant

**One authority. Multiple adapters. One evidence format. One verifier.**

```text
API / Cloud / Adapter
        |
        | submit / invoke only
        v
CANONICAL KERNEL
        |
        +-- Decision
        +-- Artifacts
        +-- Manifest
        +-- Receipt
        +-- Bundle Identity
                 |
                 v
              Verifier
```

## Authority ownership

Only the Canonical Kernel may originate or define:

- decision semantics;
- artifact semantics;
- manifest semantics;
- receipt semantics;
- canonical bundle identity.

Adapters may only submit, invoke, transport, store, or expose canonical outputs.

The verifier may only verify. It must not replay the original decision or originate alternate execution truth.

## Forbidden alternate authority

An API, cloud component, or adapter must not independently:

- create a canonical decision or execution verdict;
- create a receipt;
- define manifest semantics;
- create a canonical bundle digest;
- construct pseudo evidence presented as canonical evidence;
- reimplement policy semantics.

An API inside this repository is not a violation by location. It is a violation if it becomes an independent source of decision/evidence truth rather than a thin adapter to canonical execution.

## Enforcement model

The gate has two layers:

1. **Capability contract**: an adapter declares only allowed capabilities. Canonical-origin capabilities are rejected outside the kernel.
2. **Implementation guard**: adapter source is checked for known alternate-authority constructions as defense in depth. This guard is not the trust proof by itself.

The negative fixture deliberately requests an authority-owned capability and MUST be rejected. The positive fixture declares delegation-only capabilities and MUST pass.

## Required witness

```text
alternate authority introduced
        |
        v
architecture enforcement
        |
        v
CI FAIL (fixture is rejected)

valid adapter delegates to Canonical Kernel
        |
        v
CI PASS
```

The CI job succeeds only when both observations occur: valid adapter accepted; alternate-authority fixture rejected.

## Acceptance condition

Repository Boundary Closure is complete only when:

- valid adapter -> PASS;
- alternate authority -> REJECTED;
- current public/demo APIs do not present locally invented execution truth as canonical output;
- existing kernel determinism, artifact integrity, ledger, receipt, and verifier semantics remain unchanged;
- the boundary witness passes on the merge candidate and again on `main`.

Documentation-only changes, a submodule bump, manual review, removing `Date.now()`, or renaming demo endpoints are insufficient.

## Repository implications

- `paygod-kernel-mvp` remains the owner of canonical execution truth.
- `paygod-cloud-starter` must not originate decision/evidence semantics. Its March 2026 pseudo-execution PR is superseded by this boundary.
- `api/server.js` is currently a demo/deprecation candidate. Until a real canonical adapter is implemented, its execution-like endpoints must fail closed rather than fabricate canonical outputs.
- Updating a cloud kernel reference does not by itself prove boundary closure.

## Completion statement

Only after the witness passes may the project claim:

> Paygod has one execution authority. External interfaces delegate to it, and CI rejects alternate authorities.

That claim is **Proof of Single Authority**.

## Governance rule

> No next trust claim without a witness for the current one.

Trust sequence:

```text
Proof of Execution
        |
        v
Proof of Single Authority
        |
        v
Proof of Artifact Integrity
        |
        v
Proof of Verification Independence
        |
        v
Proof of Provenance
        |
        v
Proof of Decision Authority
        |
        v
Proof of Economic Value
```

External Verifier distribution, Provenance, and real domain authority work remain downstream of this gate.
