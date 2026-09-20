# Repository Boundary Closure v0.1

Status: **PROVEN IN CI for registered repository-hosted adapters.** PR #57 passed the merge-candidate witness, merged to `main`, and the same boundary witness passed again on merge commit `2b9be60d94eb624c16e4b05e27f92f973385680f`.

## Purpose

This gate establishes one canonical execution authority for the repository-hosted adapters that are explicitly registered in the boundary inventory. It does not forbid multiple APIs, cloud services, or adapters. It forbids registered non-canonical components from originating independent execution truth.

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

The gate has three layers:

1. **Capability contract**: an adapter declares only allowed capabilities. Canonical-origin capabilities are rejected outside the kernel.
2. **Actual adapter inspection**: every registered repository-hosted adapter must preserve its declared fail-closed or delegation boundary.
3. **Mutation witness**: copies of the actual registered adapters are injected with local verdict, receipt, and bundle-identity authority; each mutation must be rejected.

Source-level patterns remain defense in depth. They do not prove that arbitrary unregistered future code can never become an alternate authority.

## Current registered adapters

- `api/server.js` — fail closed for execution-like routes.
- `deploy/docker/api/app/Program.cs` — delegates execution to `/runner/PayGod.Cli.dll run`.

Any new execution-facing adapter must be registered in `tools/check_repository_boundary.py` and covered by the mutation witness in the same change.

## Required witness

```text
registered actual adapter unchanged
        |
        v
architecture enforcement
        |
        v
PASS

same adapter + invented verdict
same adapter + local receipt
same adapter + local bundle identity
        |
        v
architecture enforcement
        |
        v
REJECT
```

The CI job also requires the delegation-only capability fixture to pass and the alternate-authority capability fixture to be rejected.

## Acceptance condition

Repository Boundary Closure v0.1 is complete for the registered adapters when:

- valid adapter capability -> PASS;
- alternate authority capability -> REJECTED;
- current registered adapters -> PASS;
- verdict mutation -> REJECTED;
- receipt mutation -> REJECTED;
- bundle-identity mutation -> REJECTED;
- current public/demo APIs do not present locally invented execution truth as canonical output;
- existing kernel determinism, artifact integrity, ledger, receipt, and verifier semantics remain unchanged;
- the boundary witness passes on the merge candidate and again on `main`.

Those conditions passed for PR #57 and again on `main` at merge commit `2b9be60d94eb624c16e4b05e27f92f973385680f`.

## Scope limitation

This witness does **not** automatically discover every possible future execution-facing file. It is an enforcement boundary for the adapters registered in the inventory. Adding an unregistered adapter would be a governance defect and must be prevented through PR review/template requirements plus always-running boundary checks.

Documentation-only changes, a submodule bump, manual review, removing `Date.now()`, or renaming demo endpoints are insufficient substitutes for the witness.

## Repository implications

- `paygod-kernel-mvp` remains the owner of canonical execution truth.
- `paygod-cloud-starter` must not originate decision/evidence semantics. Its March 2026 pseudo-execution PR is superseded by this boundary.
- `api/server.js` remains fail closed for execution-like routes until it is replaced or made a real canonical adapter.
- Updating a cloud kernel reference does not by itself prove boundary closure.

## Completion statement

For the registered repository-hosted adapters, the project may claim:

> Paygod has one canonical execution authority. Registered repository-hosted adapters delegate to it or fail closed, and CI rejects tested alternate-authority mutations.

That claim is the scoped **Proof of Single Authority** established by Repository Boundary Closure v0.1.

## Governance rules

> No next trust claim without a witness for the current one.

> No broader claim than the witness actually proves.

> No generic infrastructure before a real workflow demands it.

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

External Verifier distribution, domain-driven Provenance, and real domain authority work remain downstream of this gate.
