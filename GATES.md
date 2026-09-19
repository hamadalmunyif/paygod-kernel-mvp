# Gates

This file describes the canonical merge and architecture gates for Paygod Kernel.

## Main-branch merge gates
- **Paygod Kernel CI** — build/test and kernel regression coverage.
- **Paygod CI Enforcement** — deterministic witness/proof enforcement.
- **Security Gate** — repository security checks.
- **Pack Contract Gate** — non-draft `pack.yaml` files must validate against the pack contract.

Other workflows may add scoped checks or witnesses.

## Evidence portability witnesses

### Portable Evidence Witness
`.github/workflows/portable-evidence.yml`

Inside CI, evidence is produced, transferred as an artifact, and independently verified across environments without replaying the original decision. Includes tamper rejection.

### Standalone Third-Party Verifier Witness
`.github/workflows/standalone-verifier.yml`

Inside CI, a recipient consumes a transferred, versioned verifier artifact and evidence bundle without repository checkout. Acceptance requires clean -> `VALID`, one-byte tamper -> `INVALID`, fail-closed behavior, and a machine-readable result.

These are CI-level witnesses, not an external-party/device trust-root proof.

## Repository Boundary Gate

`.github/workflows/repository-boundary.yml`

This gate enforces **Proof of Single Authority**. A delegation-only adapter fixture must pass; an alternate-authority fixture that claims kernel-owned decision/bundle capabilities must be rejected. Repository-hosted adapter surfaces are also checked for known local authority constructions as defense in depth.

Canonical execution truth may originate only in the kernel. APIs and cloud components may submit, invoke, transport, store, or expose canonical outputs; verifiers may verify only.

See [Repository Boundary Closure v0.1](docs/REPOSITORY_BOUNDARY.md).

## Architecture gate
The invariants in `docs/ARCHITECTURE_AUDIT.md` are the baseline. Before changing a frozen kernel primitive, explain why contracts, packs, or adapters are insufficient and preserve or explicitly version the affected verification contract.

Frozen semantics include canonicalization/digests, bundle digest construction, receipt-manifest binding, ledger hash-chain rules, deterministic pack evaluation, verifier fail-closed behavior, and the no-checkout verification boundary.

## Documentation gate
`README.md` is the public project entry point. `START_HERE.md` is canonical developer onboarding.

A material architectural change is incomplete unless README reflects what Paygod is, what is proven, current non-claims, the canonical trust path, relevant gates, and the next supported workflow.

## Product gate
After the first real domain authority pack is implemented, stop generic feature development and run a shadow pilot before adding broad platform capability.

No domain feature should silently create an alternate decision engine.
