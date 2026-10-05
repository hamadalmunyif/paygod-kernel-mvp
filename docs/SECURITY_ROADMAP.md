# Paygod Kernel Security Hardening Roadmap

This document records future security-hardening work separately from the repository's current proven assurance boundary. Roadmap items are not current capability claims unless explicitly backed by an active witness.

**Stop-build status: ACTIVE.** New security-capability expansion is paused. Only critical vulnerability remediation, preservation of existing required witnesses, and separately approved evidence-backed changes are in scope. A roadmap item is not implementation authorization.

## 1. Container Hardening (Priority: High)

**Objective:** Mitigate container breakout risks by enforcing least-privilege principles at the runtime level.

### Implementation Strategy
- **Non-Root Execution:** Keep runtime containers non-root and verify this property in the relevant container path.
- **Read-Only Filesystems:** Where production container execution becomes in-scope, prefer read-only root filesystems with explicit temporary-write locations.
- **Capability Dropping:** Where production container execution becomes in-scope, drop unnecessary Linux capabilities and add back only those explicitly required.

## 2. Supply Chain Security (Priority: High)

**Objective:** Improve reproducibility and provenance of software dependencies and build artifacts.

### Future Work
- dependency/tool version closure where reproducibility requires it;
- immutable GitHub Action references;
- broader dependency update coverage;
- artifact provenance/attestation when justified by the release workflow;
- image digest pinning when container images become release artifacts.

These are roadmap items and are not implied by the current merge-gate contract.

## 3. Image Integrity & Signing (Future)

Potential future work includes externally attested build provenance, container/image signing, and verification at deployment boundaries.

The repository does **not** currently claim universal Cosign/Sigstore release signing or production image-admission enforcement.

## 4. Key and Trust-Root Governance (Future)

Potential future work includes:
- institutional signing-key custody;
- rotation and revocation policy;
- hardware-backed or managed-key custody where justified;
- externally anchored or transparent publication where a real workflow requires it.

These are separate trust dimensions and must not be conflated with current bundle integrity.

## 5. Network and Runtime Hardening (Future)

Network segmentation, service-to-service authentication, and runtime policy are deferred until a production deployment architecture creates a concrete requirement.

---

*This roadmap is a living document. Future work must remain subordinate to the repository's stop-build rule and evidence from real workflows.*

---

## Canonical Merge Governance

The canonical merge contract is defined in [GATES.md](../GATES.md).

The required status checks for pull requests targeting `main` are:

1. **Paygod Kernel CI**
2. **security-gate**
3. **Paygod CI Enforcement**
4. **Pack Contract (paygod/v1)**
5. **Repository Boundary Gate**
6. **Verifier Integrity Gate**

Each required witness MUST report a terminal status on every pull request targeting `main`. A required witness therefore must not depend on path filtering that can prevent the required context from being emitted.

The effective GitHub repository ruleset must require these six exact contexts. A workflow being green is not sufficient if the ruleset does not require it.

### Security Gate Composition

`security-gate` is the required aggregate context for the security workflow. It propagates failures from its internal security jobs, currently including CodeQL, dependency review, secret scanning, and PR SBOM generation. Those internal job names are implementation details of the security workflow and are not substitutes for the canonical top-level merge contract above.

### Ruleset Alignment

Repository administrators must keep the active `main` ruleset aligned with [GATES.md](../GATES.md). Changes to required context names, workflow triggers, or ruleset requirements must be reviewed as governance changes.

Recommended repository protections include:
- require pull requests before merging;
- require the six canonical status checks above;
- require branches to be up to date before merging;
- prohibit force-push/non-fast-forward history on `main`;
- require additional review controls where the repository ownership model supports them.

Ruleset drift is a governance defect even when underlying workflows remain green.
