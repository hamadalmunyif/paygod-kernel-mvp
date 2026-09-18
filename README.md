# Paygod Kernel MVP

Paygod Kernel is a deterministic policy-execution core built on **contracts-first + evidence-first** principles.

It produces schema-governed decision evidence that can be transferred and independently verified without replaying the original decision.

## What is proven

The repository currently has CI witnesses for:
- bit-for-bit deterministic execution;
- schema-governed evidence artifacts;
- receipt-to-manifest and bundle-digest binding;
- CI-enforced contract, determinism, and security gates;
- artifact-only evidence handoff across environments;
- Linux-producer to Windows-verifier portability;
- standalone/no-checkout verification inside CI;
- fail-closed rejection after a one-byte evidence mutation.

The standalone verifier checks manifest integrity, artifact SHA-256 digests, bundle-digest binding, receipt binding, and ledger hash-chain integrity where present.

## What is not yet proven

The repository does **not** yet prove:
- that an external real-world fact or claimed evidence issuer is truthful;
- a published/signed external verifier trust root;
- an external-device/party verification witness outside repository CI;
- a live bank/PSP release integration;
- autonomous authority over money movement;
- institutional adoption or willingness to pay.

**Integrity is not provenance.**

## Canonical trust path

```text
External fact/source
        |
        v
Evidence / provenance
        |
        v
Contract + Policy Pack
        |
        v
Deterministic Kernel
        |
        v
Decision Artifact
        |
        v
Manifest + Receipt + Ledger
        |
        v
Portable Evidence Bundle
        |
        v
Independent Verifier
```

Execution rails such as a bank, PSP, agent, or API are downstream consumers; they are not part of the kernel trust primitive.

## Architecture

```text
CLI -> Canonicalization -> Pack Evaluation -> Artifact Envelope -> Receipt/Ledger -> Witness -> CI Gate
```

Domain logic should enter through contracts, packs, or adapters before changing kernel semantics.

See [Architecture Audit](docs/ARCHITECTURE_AUDIT.md).

## Quickstart

Canonical developer onboarding: [START_HERE.md](START_HERE.md).

```bash
dotnet publish src/PayGod.Cli/PayGod.Cli.csproj -c Release -o out
```

```powershell
pwsh -NoProfile -File ./tools/phase4_docker_witness.ps1
```

Expected: `PASS` (strict) with matching digests.

## Portable verification

- `.github/workflows/portable-evidence.yml` — artifact handoff and cross-OS independent verification.
- `.github/workflows/standalone-verifier.yml` — versioned standalone verifier artifact, no repository checkout in recipient jobs, clean evidence -> `VALID`, one-byte tamper -> `INVALID`.

See [Standalone Verifier](docs/STANDALONE_VERIFIER.md).

## Main-branch enforcement

See [GATES.md](GATES.md). Core merge gates include Paygod Kernel CI, Paygod CI Enforcement, Security Gate, and Pack Contract Gate. Portability workflows provide additional architectural witnesses and regression protection.

## Next boundary

1. Package and test the verifier outside repository CI.
2. Define Evidence Provenance Contract v0.1.
3. Implement one bounded real-domain authority pack.
4. Stop generic feature development.
5. Run a shadow pilot against real human decisions.

First candidate:

```text
invoice + PO + facility state + collateral/evidence + policy
                         |
                         v
              RELEASE / REDUCE / HOLD
                         |
                         v
                       receipt
```

See [ROADMAP.md](ROADMAP.md).
