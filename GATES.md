# Gates

This file describes the canonical merge and architecture gates for Paygod Kernel.

## Required merge-gate contract

The main branch governance contract is that every pull request to `main` reports these stable check contexts, and the GitHub ruleset requires them before merge:

- **Paygod Kernel CI** — build/test and kernel regression coverage.
- **security-gate** — aggregate repository security gate.
- **Paygod CI Enforcement** — deterministic witness/proof enforcement.
- **Pack Contract (paygod/v1)** — non-draft `pack.yaml` files validate against the pack contract.
- **Repository Boundary Gate** — registered repository-hosted adapters preserve the canonical single-authority boundary.

During migration, the CI-enforcement workflow also emits a temporary legacy `enforce` compatibility context. Keep it until any classic branch-protection dependency on that historical name is explicitly verified absent; the readable repository ruleset itself must require `Paygod CI Enforcement`.

A gate that is intended to be required must run on every pull request to `main`; path-filtered required checks can otherwise leave unrelated pull requests waiting for a check that never starts.

The GitHub ruleset must be kept aligned with these stable contexts. Ruleset drift is a governance defect, even when the underlying workflows remain green.

## Evidence portability witnesses

### Portable Evidence Witness
`.github/workflows/portable-evidence.yml`

Inside CI, evidence is produced, transferred as an artifact, and independently verified across environments without replaying the original decision. Includes tamper rejection.

### Standalone Third-Party Verifier Witness
`.github/workflows/standalone-verifier.yml`

Inside CI, a recipient consumes a transferred, versioned verifier artifact and evidence bundle without repository checkout. Current v0.2 acceptance requires clean -> `VALID`, payload tamper -> `INVALID`, decision-critical receipt tamper -> `INVALID`, a missing manifest-locked ledger -> `INVALID`, malformed control data -> machine-readable `INVALID`, and supported default-clock output to remain verifiable without claiming injected-time binding.

These are CI-level witnesses, not an external-party/device trust-root proof.

## Repository Boundary Gate

`.github/workflows/repository-boundary.yml`

This gate enforces the single-authority boundary for **registered repository-hosted adapters**. A delegation-only adapter fixture must pass; an alternate-authority fixture must be rejected; the actual registered adapter implementations must pass inspection; and verdict, receipt, and bundle-identity mutations of those implementations must be rejected.

Canonical execution truth may originate only in the kernel. APIs and cloud components may submit, invoke, transport, store, or expose canonical outputs; verifiers may verify only.

The current witness is scoped to adapters registered in `tools/check_repository_boundary.py`. Any new execution-facing adapter must be registered and covered by the mutation witness in the same change.

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
