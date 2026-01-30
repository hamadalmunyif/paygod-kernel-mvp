# Paygod Kernel Security Hardening Roadmap

This document outlines the strategic security enhancements required to elevate Paygod Kernel from a functional prototype to a production-grade, high-assurance financial system.

## 1. Container Hardening (Priority: High)

**Objective:** Mitigate container breakout risks by enforcing least-privilege principles at the runtime level.

### Implementation Strategy
- **Non-Root Execution:** Modify all Dockerfiles to create and switch to a dedicated user (e.g., `app`) before the `ENTRYPOINT` instruction.
- **Read-Only Filesystems:** Configure `docker-compose.yml` and Kubernetes manifests to mount the root filesystem as read-only (`read_only: true`). Use explicit `tmpfs` mounts for temporary directories required by the runtime.
- **Capability Dropping:** Explicitly drop all Linux capabilities (`cap_drop: [ALL]`) and only add back strictly necessary ones (if any).

## 2. Supply Chain Security (Priority: High)

**Objective:** Ensure the integrity of all software dependencies and build artifacts.

### Implementation Strategy
- **Vulnerability Scanning:** Integrate **Trivy** or **Grype** into the CI pipeline to scan base images and NuGet/Python packages for known CVEs before every build.
- **SBOM Generation:** Automatically generate a Software Bill of Materials (SBOM) for every release artifact to facilitate rapid impact analysis during security incidents.
- **Dependency Pinning:** Enforce strict version pinning (including hashes) for all dependencies in `csproj` and `requirements.txt` files.

## 3. Image Integrity & Signing (Priority: Medium)

**Objective:** Prevent the deployment of unauthorized or tampered container images.

### Implementation Strategy
- **Cosign Integration:** Use **Sigstore Cosign** to cryptographically sign container images immediately after the build phase in the CI pipeline.
- **Admission Controllers:** Deploy a Kubernetes Admission Controller (e.g., Kyverno or OPA Gatekeeper) to verify image signatures before allowing pods to start.

## 4. Cryptographic Ledger Locking (Priority: Critical)

**Objective:** Protect the immutable ledger against retroactive tampering, even in the event of a key compromise.

### Implementation Strategy
- **HSM Integration:** Transition signing keys from software-based storage to Hardware Security Modules (HSM) or managed cloud KMS (Key Management Service).
- **Key Rotation Policy:** Implement automated key rotation for ledger signing keys.
- **Checkpointing:** Periodically publish the latest ledger root hash to a public, decentralized blockchain (e.g., Ethereum or Bitcoin) to serve as an indisputable timestamp proof.

## 5. Network Segmentation (Priority: Medium)

**Objective:** Limit the blast radius of a potential breach by strictly controlling network traffic.

### Implementation Strategy
- **Service Mesh:** Implement mTLS (mutual TLS) between all microservices (Kernel, Ledger, Metrics) to ensure encrypted and authenticated communication.
- **Network Policies:** Apply strict Kubernetes Network Policies to deny all ingress/egress traffic by default, whitelisting only necessary communication paths.

---

*This roadmap is a living document. Security is a continuous process, not a final destination.*

---

## PR Security Gate (GitHub Actions + Branch Protection)

Paygod Kernel treats security checks as **merge-blocking** on `main`.

### Workflows

- `Paygod Kernel CI` — build, spec checks, schema stability, pack tests, and pack-provider separation lint.
- `security-gate` — CodeQL, Dependency Review, secret scanning, and PR SBOM artifact.

### Required Checks (Branch Protection)

In GitHub: **Settings → Branches → Branch protection rules → main**, enable:

- **Require status checks to pass before merging**
- Select the checks below (names must match exactly):

1) **CodeQL (C#)**
2) **Dependency Review (PR)**
3) **Secret Scan (gitleaks)**
4) **SBOM (PR artifact)**
5) **build-and-test** (from `Paygod Kernel CI`)

Recommended toggles:
- Require branches to be up to date before merging
- Require signed commits (if your org enforces it)
- Require approvals (CODEOWNERS-driven)

### Notes

- Dependency Review runs **only** on pull requests by design.
- PR SBOM is uploaded as an artifact for transparency; release SBOM is still produced on tags.
- Container scanning is intentionally deferred until Docker images become a first-class MVP deliverable.

## Making the Security Gate truly merge-blocking (Branch Protection)

Workflows alone **do not** prevent merging. To make the Security Gate a real PR Gate, you must
enable **Branch Protection** on `main` and set **Required status checks** to include the security
jobs and CI build/test.

### Required checks (job names must match exactly)
- `CodeQL (C#)`
- `Dependency Review (PR)`
- `Secret Scan (gitleaks)`
- `SBOM (PR artifact)`
- `CI`

### Fast path (recommended): apply via GitHub CLI
If you have repo admin rights, run:

```bash
gh auth login
export REPO="OWNER/REPO"
export BRANCH="main"
./tools/admin/enable_branch_protection.sh
```

### Manual path (UI)
GitHub → **Settings** → **Branches** → **Add rule** for `main`:
- ✅ Require a pull request before merging
- ✅ Require status checks to pass before merging
  - add the required checks listed above
- ✅ Require branches to be up to date before merging (recommended)
- ✅ Require Code Owner review (recommended)
